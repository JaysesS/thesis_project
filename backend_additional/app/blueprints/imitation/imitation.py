from logging import getLogger
from flask.views import MethodView
from flask import Blueprint, jsonify, redirect, url_for, render_template
from flask import current_app

from blueprints.helpers import login_required

from models import User

logger = getLogger("THESIS")

imitation_bp = Blueprint(
                        'imitation', __name__,
                        url_prefix='/',
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='imitation/static'
                    )



class IndexView(MethodView):

    methods = ['GET']

    def get(self):

        # def has_no_empty_params(rule):
        #     defaults = rule.defaults if rule.defaults is not None else ()
        #     arguments = rule.arguments if rule.arguments is not None else ()
        #     return len(defaults) >= len(arguments)
        # links = []
        # for rule in current_app.url_map.iter_rules():
        #     # Filter out rules we can't navigate to in a browser
        #     # and rules that require parameters
        #     if "GET" in rule.methods and has_no_empty_params(rule):
        #         url = url_for(rule.endpoint, **(rule.defaults or {}))
        #         links.append((url, rule.endpoint))

        # return jsonify(map = links)
        return redirect(url_for('login.login'))

class Imitation(MethodView):
    
    methods = ['GET', 'POST']

    @login_required
    def get(self):
        return render_template("cabinet.html")

    @login_required
    def post(self):
        return jsonify(status = True, message = "post")


index_page = IndexView.as_view('index')
imitation_page = Imitation.as_view('imitation')

imitation_bp.add_url_rule("/", view_func=index_page)
imitation_bp.add_url_rule("/cabinet", view_func=imitation_page)

