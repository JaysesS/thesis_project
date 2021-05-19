from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired,ValidationError

from models import User

class BaseForm(FlaskForm):
    
    class Meta:
        csrf = False

    _register = False

    def to_dict(self):
        return {key : value.data for key, value in dict(self._fields).items()}


class UsernameForm(BaseForm):

    _user = None
    username = StringField("Username", validators=[InputRequired()])
    
    def get_user_by_username(self):
        return User.get_user_by_username(self.username.data)

    def validate_username(self, field):
        self._user = self.get_user_by_username()

        if self._register:
            if self._user is not None:
                raise ValidationError("Пользователь с таким логином уже зарегистрирован")
        else:
            if self._user is None:
                raise ValidationError('Пользователь не найден')

class PasswordForm(BaseForm):

    password = PasswordField("Password", validators=[InputRequired()])

    def validate_password(self, field):
        if not self._register:
            if self._user is None or not self._user.check_password(self.password.data):
                raise ValidationError('Некорректный пароль')


class LoginForm(UsernameForm, PasswordForm):
    """ Login Form """

class RegisterForm(UsernameForm, PasswordForm):

    """ Register Form """

    _register = True
