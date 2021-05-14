from flask import redirect, url_for, abort, flash, request
from flask_admin import AdminIndexView, expose, helpers
from flask_admin.actions import action
from admin.form import MyInlineModelForm, LoginForm
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, utils
from wtforms import fields
from models import db, User, RolesUsers, Role

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
        if helpers.validate_form_on_submit(flask_form):
            user = flask_form.get_user()
            utils.login_user(user)
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['flask_form'] = flask_form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        utils.logout_user()
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
    column_exclude_list = ('password',)
    inline_models = (MyInlineModelForm(RolesUsers, db.session),)

    form_excluded_columns = ('password', 'roles')
    column_auto_select_related = True
    form_widget_args = {
        'password2': {
            'autocomplete': 'new-password'
        }
    }

    column_searchable_list = ("username",)

    @action('refresh_token', 'Refresh Token', 'Обновить токен(-ы)?')
    def action_refresh_token(self, ids):
        try:
            users = User.query.filter(User.id.in_(ids)).all()
            for user in users:
                user.set_token()
                user.save_to_db()
        except Exception as ex:
            flash(f'Failed to approve users. {str(ex)}', 'error')

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
    (MyModelView, Role, dict(category='Пользователи'))
]

def init_views():
    return [ view(model, db.session, **settings) for view, model, settings in model_views_map]