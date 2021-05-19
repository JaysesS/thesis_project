from logging import getLogger, log
from flask.views import MethodView
from flask import Blueprint
from flask import jsonify
from flask_security import login_required

from models import User

logger = getLogger("THESIS")

imitation_bp = Blueprint(
                        'imitation', __name__,
                        url_prefix='/',
                        template_folder="templates",
                    )

class Imitation(MethodView):
    
    methods = ['GET', 'POST']

    @login_required
    def get(self):
        return jsonify(status = True, message = "get")

    @login_required
    def post(self):
        return jsonify(status = True, message = "post")

imitation_page = Imitation.as_view('imitation')

imitation_bp.add_url_rule("/auth", view_func=imitation_page)

