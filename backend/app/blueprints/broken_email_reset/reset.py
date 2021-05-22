from logging import getLogger
import jwt
import datetime
from flask import current_app
from flask.views import MethodView
from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_security import current_user, login_user, login_required

from blueprints.broken_email_reset.helpers import logout_before
from blueprints.forms import ResetForm, ResetPasswordsForm
from utils.mail_sender import send_email
from models import User

logger = getLogger("THESIS")

# Template folder is os.path.dirname(os.path.abspath(__file__)) + template_folder ("templates")
reset_bp = Blueprint(
                        'reset', __name__,
                        url_prefix='/',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='reset/static'
                    )

class ResetBase(MethodView):

    methods = ['GET', 'POST']

    is_vuln = False
    
    def get(self):
        form = ResetForm()
        return render_template("reset_problem.html", is_vuln = self.is_vuln, form = form)


class ResetVuln(ResetBase):

    is_vuln = True
    
    def post(self):
        form = ResetForm()
        if form.validate_on_submit():
            data = form.to_dict()

            """
                Уязвимая генерация ссылки восстановления
            """
            user = User.get_user_by_username(data.get('username'))
            email = user.email
            hash = user.weak_token
            reset_url = f"http://{current_app.config.get('HOST_IP')}{current_app.config.get('APP_PREFIX')}/reset_problem/vuln/reset/{hash}"
            
            template = render_template("email_template.html", reset_password_link = reset_url)
            send_email(subject="Thesis project | Reset password", body_text="", html = template, to_addr=email)
            return redirect(url_for('reset.reset_password_vuln'))
        return render_template("reset_problem.html", is_vuln = self.is_vuln, form = form)


class ResetSecurity(ResetBase):

    is_vuln = False

    def post(self):
        form = ResetForm()
        if form.validate_on_submit():
            data = form.to_dict()
            user = User.get_user_by_username(data.get('username'))
            email = user.email
            
            jwt_payload = jwt.encode(
                {
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                    "username" : data.get('username')
                }, 
                current_app.config.get("JWT_KEY")
            )

            reset_url = f"http://{current_app.config.get('HOST_IP')}{current_app.config.get('APP_PREFIX')}/reset_problem/secure/reset/{jwt_payload}"

            template = render_template("email_template.html", reset_password_link = reset_url)
            send_email(subject="Thesis project | Reset password", body_text="", html = template, to_addr=email)
            return redirect(url_for('reset.reset_password_secure'))
        return render_template("reset_problem.html", is_vuln = self.is_vuln, form = form)


class ResetPasswordBase(MethodView):

    methods = ['GET', 'POST']

    is_vuln = False

    @login_required
    def post(self, hash):
        form = ResetPasswordsForm()
        if form.validate_on_submit():
            data = form.to_dict()
            current_user.set_password(data.get('password'))
            current_user.save_to_db()
            flash('Пароль успешно изменён!', category="success")
            return redirect(url_for('index.index'))
        return render_template("reset_wait.html", is_vuln = self.is_vuln, state = 2, form = form)


class ResetPasswordVuln(ResetPasswordBase):

    is_vuln = True

    def get(self, hash):
        form = ResetPasswordsForm()
        if hash is None:
            return render_template("reset_wait.html", is_vuln = self.is_vuln, state = 1, form = form)
        login_user(User.get_user_by_weak_hash(hash))
        return render_template("reset_wait.html", is_vuln = self.is_vuln, state = 2, form = form)


class ResetPasswordSecurity(ResetPasswordBase):

    is_vuln = False
    
    def get(self, hash):
        form = ResetPasswordsForm()
        
        if hash is None:
            return render_template("reset_wait.html", is_vuln = self.is_vuln, state = 1, form = form)

        try:
            decoded = jwt.decode(hash, current_app.config.get("JWT_KEY"), algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            flash("Токен недействителен!", category="danger")
            return redirect(url_for("index.index"))

        user = User.get_user_by_username(decoded.get("username"))
        login_user(user)
        return render_template("reset_wait.html", is_vuln = self.is_vuln, state = 2, form = form)


reset_index = ResetBase.as_view('reset')
reset_vuln_page = ResetVuln.as_view('reset_vuln')
reset_vuln_wait = ResetPasswordVuln.as_view('reset_password_vuln')

reset_sec_page = ResetSecurity.as_view('reset_secure')
reset_sec_wait = ResetPasswordSecurity.as_view('reset_password_secure')

reset_bp.add_url_rule("/reset_problem/", view_func=reset_index)

reset_bp.add_url_rule("/reset_problem/vuln/", view_func=reset_vuln_page)
reset_bp.add_url_rule("/reset_problem/vuln/reset/", view_func=reset_vuln_wait, defaults = {"hash" : None})
reset_bp.add_url_rule("/reset_problem/vuln/reset/<string:hash>", view_func=reset_vuln_wait)

reset_bp.add_url_rule("/reset_problem/secure/", view_func=reset_sec_page)
reset_bp.add_url_rule("/reset_problem/secure/reset/", view_func=reset_sec_wait, defaults = {"hash" : None})
reset_bp.add_url_rule("/reset_problem/secure/reset/<string:hash>", view_func=reset_sec_wait)
