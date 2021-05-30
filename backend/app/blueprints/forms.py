from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
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

class EmailForm(BaseForm):

    email = StringField("Email", validators=[InputRequired()])

    def get_user_by_email(self):
        return User.get_user_by_email(self.email.data)

    def validate_email(self, field):
        self._user = self.get_user_by_email()
        if self._register and self._user:
            raise ValidationError("Пользователь с такой почтой уже зарегистрирован")
        elif self._user is None and not self._register:
            raise ValidationError('Пользователь c такой почтой не найден')


class ResetForm(UsernameForm, EmailForm):
    """ Reset Form """

class ResetPasswordsForm(BaseForm):

    _register = True
    password = PasswordField("Password", validators=[InputRequired()])
    password_second = PasswordField("Password", validators=[InputRequired()])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if self.password.data != self.password_second.data:
            self.password.errors.append('Пароли не совпадают!')
            return False

        return True


class LoginForm(UsernameForm, PasswordForm):
    """ Login Form """

class RegisterForm(UsernameForm, PasswordForm, EmailForm):

    """ Register Form """

    _register = True


class PostForm(BaseForm):

    author = StringField("Author", validators=[InputRequired()])
    text = TextAreaField('Comment', validators = [InputRequired()])