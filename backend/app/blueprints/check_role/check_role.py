from flask.helpers import flash
from flask.views import MethodView
from flask import Blueprint, render_template
from flask_security import roles_required
from logging import getLogger

logger = getLogger("THESIS")

class RoleView(MethodView):
    
    methods = ['GET']
    
    @roles_required('admin')
    def get(self):
        flash('Успешное прохождение проверки роли!', "success")
        return render_template("check_roles.html")

check_role_bp = Blueprint(
                        'check_role', __name__,
                        url_prefix='/',
                        template_folder="templates"
                    )




check_role_page = RoleView.as_view('index')

check_role_bp.add_url_rule("/role_check", view_func=check_role_page)