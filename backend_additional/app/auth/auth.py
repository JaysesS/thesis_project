from flask_security import Security, SQLAlchemyUserDatastore
from flask import jsonify, url_for

from models import db, User, Role

def init_login(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    
    @security.login_manager.request_loader
    def load_user_from_request(req):
        token = req.headers.get('Authorization')
        if token:
            user = User.query.filter_by(token=token).first()
            if user and user.is_active:
                return user
        return None

    @security.unauthorized_handler
    def unauth_handler():
        return jsonify(success=False,
                       message='Authorize please to access this page.'), 403

def _init_instance(cls, list_name):
    for instance_name in list_name:
        instance = cls.query.filter_by(name=instance_name).first()
        if not instance:
            instance = cls(name=instance_name)
            db.session.add(instance)
            db.session.commit()
    return instance

def test_user_setup(app):
    role = _init_instance(Role, ('user', 'admin'))
    user = User.get_user_by_username("jayse")
    if not user:
        user = User.register_user("jayse", 1337)
        user.roles.append(Role.get_role_by_name("user"))
    if role not in user.roles:
        user.roles.append(role)
    db.session.add(user)
    db.session.commit()

