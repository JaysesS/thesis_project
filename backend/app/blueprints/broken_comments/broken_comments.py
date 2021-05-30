from logging import getLogger
from flask.helpers import flash
from flask.views import MethodView
from flask import Blueprint, render_template, request

from models import User

logger = getLogger("THESIS")

xss_bp = Blueprint(
                        'xss', __name__,
                        url_prefix='/',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='xss/static'
                    )

class XSSDemostration(MethodView):

    methods = ['GET', 'POST']
    
    def get(self):
        return render_template("broken_comments.html")
    
    def post(self):
        return 1

index_sql = XSSDemostration.as_view('xss_index')

xss_bp.add_url_rule("/xss", view_func=index_sql)
