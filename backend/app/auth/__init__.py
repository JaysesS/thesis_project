from flask_security import Security, SQLAlchemyUserDatastore
from flask import jsonify

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