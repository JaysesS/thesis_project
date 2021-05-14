from flask import session
from flask_security import current_user
from flask_security.decorators import roles_accepted
from flask import jsonify, make_response, abort, redirect, url_for, flash
from functools import wraps

def role_required(role):
    def _role_required(func):
        @wraps(func)
        @roles_accepted(role)
        def wrapper(*args, **kwargs):
            if not current_user.check_role_time(role):
                abort(make_response(jsonify(message="Role expires!"), 401))
            return func(*args, **kwargs)
        return wrapper
    return _role_required

def redirect_auth_to(path):
    def _redirect_auth_to(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            if not current_user.is_anonymous:
                return redirect(url_for(path))
            return func(*args, **kwargs)
        return _wrapper
    return _redirect_auth_to

def reject_anonymous(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for("login.login"))
        return func(*args, **kwargs)
    return _wrapper

def reject_anonymous_flash_login(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            flash("Для продолжения необходима аутентификация!", category="danger")
            return redirect(url_for("login.login"))
        return func(*args, **kwargs)
    return _wrapper