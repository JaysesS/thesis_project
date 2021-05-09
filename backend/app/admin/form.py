from flask_security import current_user
from wtforms import form, fields, validators
from flask_admin.model.form import InlineFormAdmin
from models import User, Role

class LoginForm(form.Form):
    name = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_name(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not user.check_password(self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.query.filter_by(name=self.name.data).first()

class MyInlineModelForm(InlineFormAdmin):

    def __init__(self, models, session, **kwargs):
        super(MyInlineModelForm, self).__init__(models, **kwargs)
        self.session = session
        if self.form_args:
            self.form_args.update({
                "roles": dict(label="Roles", query_factory=self.filtering_function)
            })
        else:
            self.form_args = {
                "role": dict(label="Role", query_factory=self.filtering_function)
            }

    def filtering_function(self):
        if current_user.has_role('admin'):
            role_filter = True
        else:
            role_filter = Role.name != 'admin'
        return self.session.query(Role).filter(role_filter)