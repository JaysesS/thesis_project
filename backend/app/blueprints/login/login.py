from logging import getLogger
from flask.views import MethodView
from flask import Blueprint, redirect, url_for, render_template
from flask_security import current_user, logout_user, login_user
from flask import session

from blueprints.forms import LoginForm, RegisterForm
from models import User

logger = getLogger("THESIS")

login_bp = Blueprint(
                        'login', __name__,
                        url_prefix='/',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='login/static'
                    )

class Login(MethodView):
    
    methods = ['GET', 'POST']

    def get(self):
        form = LoginForm()
        return render_template("login.html", form = form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = form.get_user_by_username()
            login_user(user)
            return redirect(url_for('index.index'))
        return render_template("login.html", form = form)

class Register(MethodView):
    
    methods = ['GET', 'POST']

    def get(self):
        form = RegisterForm()
        return render_template("register.html", form = form)

    def post(self):
        form = RegisterForm()
        if form.validate_on_submit():
            print("good")
            User.register_user(**form.to_dict())
            return redirect(url_for("login.login"))
        return render_template("register.html", form = form)

class Logout(MethodView):
    
    methods = ['GET']

    def get(self):
        logout_user()
        session.clear()
        return redirect(url_for('login.login'))

login_page = Login.as_view('login')
reg_page = Register.as_view('register')
logout_page = Logout.as_view('logout')


login_bp.add_url_rule("/login", view_func=login_page)
login_bp.add_url_rule("/register", view_func=reg_page)
login_bp.add_url_rule("/logout", view_func=logout_page)
