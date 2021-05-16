from functools import wraps
from flask import session, redirect, url_for, flash
from flask_security import current_user, logout_user

def logout_before(state):
    def _logout_before(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_anonymous:
                logout_user()
                session.clear()
                flash('Авторизация была сброшена', category="success")
                return redirect(url_for(state))
            return func(*args, **kwargs)
        return wrapper
    return _logout_before