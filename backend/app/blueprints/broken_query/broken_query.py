from logging import getLogger
from flask.helpers import flash
from flask.views import MethodView
from flask import Blueprint, render_template, request
from blueprints.broken_query.operations import sqli_query

from models import User

logger = getLogger("THESIS")

sqli_bp = Blueprint(
                        'sqli', __name__,
                        url_prefix='/',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='sqli/static'
                    )

class SQLiDemostration(MethodView):

    methods = ['GET', 'POST']
    
    def get(self):
        return render_template("broken_sqli.html", query_result = False)
    
    def post(self):
        form_type = request.form.get("form_type")
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if form_type == "vuln":
            query_result = sqli_query(
                username=username,
                password=password
            )
        elif form_type == "secure":
            user = User.get_user_by_username(username)
            query_result = user.to_list() if user and user.password == password else []
        else:
            flash("Зачем менять вид формы?")
            query_result = ""
        
        if isinstance(query_result, list) and len(query_result) == 0:
            flash("Ничего не найдено", "danger")

        return render_template("broken_sqli.html", query_result = query_result)

index_sql = SQLiDemostration.as_view('sqli_index')

sqli_bp.add_url_rule("/sqli", view_func=index_sql)
