from flask import redirect, url_for
from flask_security import current_user
from functools import wraps

def login_required(func):
    @wraps(func)
    def _wrapper(self, *a, **k):
        if current_user.is_anonymous:
            return redirect(url_for("login.login"))
        return func(self, *a, **k)
    return _wrapper