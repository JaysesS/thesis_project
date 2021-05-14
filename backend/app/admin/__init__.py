import flask_admin
import os
from models import db, User, Role
from admin.view import MyAdminIndexView, init_views

def _init_instance(cls, list_name):
    for instance_name in list_name:
        instance = cls.query.filter_by(name=instance_name).first()
        if not instance:
            instance = cls(name=instance_name)
            db.session.add(instance)
            db.session.commit()
    return instance

def _init_catalogs(test=False):
    role = _init_instance(Role, ('manager', 'admin'))
    if test:
        admin_user = User.get_user_by_username(username="admin") #User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin')
        admin_user.set_password('123')
    else:
        admin_user = User.get_user_by_username(username=os.environ.get("POSTGRES_USER"))
        if not admin_user:
            admin_user = User(username=os.environ.get("POSTGRES_USER"))
        admin_user.set_password(os.environ.get("POSTGRES_PASSWORD"))
    
    if role not in admin_user.roles:
        admin_user.roles.append(role)
    db.session.add(admin_user)
    db.session.commit()

def init_admin(app):
    index_view = MyAdminIndexView(url='/admin/')
    admin = flask_admin.Admin(app, index_view = index_view, base_template = '_master.html', template_mode = 'bootstrap4')
    admin.add_views(*init_views())