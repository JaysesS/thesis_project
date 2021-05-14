from logging import getLogger
from flask.views import MethodView
from flask import Blueprint, render_template, session

from utils.decorators import reject_anonymous_flash_login
from blueprints.forms import ResetForm
from utils.mail_sender import send_email

logger = getLogger("THESIS")

# Template folder is os.path.dirname(os.path.abspath(__file__)) + template_folder ("templates")
reset_bp = Blueprint(
                        'reset', __name__,
                        url_prefix='/reset_problem',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='reset/static'
                    )


class ResetProblem(MethodView):
    
    methods = ['GET', 'POST']
    
    
    @reject_anonymous_flash_login
    def get(self):
        form = ResetForm()
        return render_template("reset_problem.html", form = form)

    @reject_anonymous_flash_login
    def post(self):
        form = ResetForm()
        if form.validate_on_submit():
            data = form.to_dict()
            send_email(subject="RESET)", body_text=f"Уважаемый {data.get('username')} рестарни пароль!\n *супер линк*", to_addr="softelele@mail.ru")
        return render_template("reset_problem.html", form = form)


reset_page = ResetProblem.as_view('reset_problem')

reset_bp.add_url_rule("/", view_func=reset_page)