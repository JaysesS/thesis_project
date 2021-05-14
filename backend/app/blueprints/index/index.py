from logging import getLogger
from flask.views import MethodView
from flask import Blueprint, render_template

logger = getLogger("THESIS")

index_bp = Blueprint(
                        'index', __name__,
                        url_prefix='/',
                        template_folder="templates"
                    )


class IndexView(MethodView):
    
    methods = ['GET']
    
    def get(self):
        return render_template("index.html")


index_page = IndexView.as_view('index')

index_bp.add_url_rule("/", view_func=index_page)
index_bp.add_url_rule("/index", view_func=index_page)