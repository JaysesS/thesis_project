from logging import getLogger
from flask.views import MethodView
from flask import Blueprint, render_template, jsonify
from flask_security import current_user, logout_user, login_user
from blueprints.broken_sqli.operations import check

from models import db, User

logger = getLogger("THESIS")

sqli_bp = Blueprint(
                        'sqli', __name__,
                        url_prefix='/',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='sqli/static'
                    )

class Demostration(MethodView):

    methods = ['GET']
    
    def get(self):
        # print(User.__table__.columns.keys())

        check()
        
        return render_template("broken_sqli.html")

class SQLiView(MethodView):
    
    methods = ['POST']
    
    def post(self):
        return jsonify(status = True)


index_sql = Demostration.as_view('sqli_index')

sqli_bp.add_url_rule("/sqli", view_func=index_sql)
# sqli_bp.add_url_rule("/index", view_func=index_page)