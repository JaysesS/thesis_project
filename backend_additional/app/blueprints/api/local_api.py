from os import access
from flask.views import MethodView
from flask import Blueprint, current_app, json, jsonify, request
from flask_security import current_user
from blueprints.helpers import login_required
from models import User

api_bp = Blueprint(
                        'api', __name__,
                        template_folder="templates",
                        static_folder='static',
                        static_url_path='imitation/static'
                    )

class LocalApiUser(MethodView):
    
    methods = ['GET', 'POST']

    @login_required
    def get(self):
        return jsonify(status=True, username = current_user.username, token = current_user.token)

    @login_required
    def post(self):
        data = request.get_json()
        current_user.token = data.get("token")
        current_user.save_to_db()
        return jsonify(status = True, username = current_user.username, token = data.get("token"))

class OutsideApiUser(MethodView):

    methods = ['GET']

    def get(self):
        data = request.args
        access_token = data.get("access_token")
        if access_token != current_app.config.get("MAIN_ACCESS_TOKEN"):
            return jsonify(status=False, message = "Incorrect access token!")
        user = User.get_user_by_username(data.get("username"))
        if user and user.token == data.get("token"):
            return jsonify(status=True, verify = True)
        return jsonify(status=True, verify = False)

api_user = LocalApiUser.as_view('api_user')
api_outside_user = OutsideApiUser.as_view('api_outside_user')

api_bp.add_url_rule("/user", view_func=api_user)
api_bp.add_url_rule("/outside_user", view_func=api_outside_user)