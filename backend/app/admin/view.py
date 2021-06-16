from flask import redirect, url_for, abort, flash, request
from flask_admin import AdminIndexView, expose, helpers
from flask_admin.actions import action
from admin.form import MyInlineModelForm, LoginForm
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, login_user, logout_user
from wtforms import fields
from models import db, User, RolesUsers, Role, Post
import logging


logger = logging.getLogger("THESIS")

class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        flask_form = LoginForm(request.form)
        if flask_form.validate_on_submit():
            user = flask_form.get_user()
            print(user)
            if user and user.password == flask_form.password.data:
                login_user(user)
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['flask_form'] = flask_form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

class MyModelView(ModelView):
    def __init__(self, model, session, roles=None, **kwargs):
        super().__init__(model, session, **kwargs)
        if roles:
            self.roles = roles
        else:
            if not hasattr(self, 'roles'):
                self.roles = []

    def is_accessible(self):
        return current_user.has_role('admin', *self.roles)

class UserModelView(MyModelView):
    roles = ['manager']
    # column_exclude_list = ('password',)
    inline_models = (MyInlineModelForm(RolesUsers, db.session),)

    form_excluded_columns = ('password', 'roles')
    column_auto_select_related = True
    form_widget_args = {
        'password2': {
            'autocomplete': 'new-password'
        }
    }

    column_searchable_list = ("username",)

    def get_query(self):
        if not current_user.has_role("admin"):
            return super(UserModelView, self).get_query().filter(~self.model.roles.any(Role.name.like('admin')))
        return super(UserModelView, self).get_query()

    def scaffold_form(self):
        form_class = super(UserModelView, self).scaffold_form()
        form_class.password2 = fields.PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        if len(form.password2.data):
            model.set_password(form.password2.data)

    def on_form_prefill(self, form, id):
        if not current_user.has_role('admin') and User.query.get(id).has_role('admin'):
            abort(403)

model_views_map = [
    (UserModelView, User, dict(category='Пользователи')),
    (MyModelView, Role, dict(category='Пользователи')),
    (MyModelView, Post, dict(category='Комментарии')),
]

def init_views():
    return [ view(model, db.session, **settings) for view, model, settings in model_views_map]