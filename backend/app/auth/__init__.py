from flask_security import Security, SQLAlchemyUserDatastore
from flask import flash, redirect, url_for

from models import db, User, Role

def init_login(app):
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @security.unauthorized_handler
    def unauth_handler():
        flash("Просмотр данной страницы доступен только администратору!", "danger")
        return redirect(url_for('index.index'))