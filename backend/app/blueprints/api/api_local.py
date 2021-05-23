from logging import getLogger
import requests
from flask.views import MethodView
from flask import Blueprint, jsonify, request, current_app

logger = getLogger("THESIS")

api_bp = Blueprint(
                        'api', __name__,
                        url_prefix='/',
                        template_folder="templates"
                    )

def verify_user(url_path, username, token):
    if not current_app.config.get("LOCAL"):
        url_path = "http://backend_additional:5100/"
    url = f"{url_path}backend_additional/api/outside_user"
    res = requests.get(url, params= {
        "access_token" : current_app.config.get("BACKEND_ADDITIONAL_TOKEN"),
        "username" : username,
        "token" : token
    }).json()
    return True if res.get("verify") else False

class ServiceView(MethodView):
    
    methods = ['GET']
    
    def get(self):
        data = request.args
        if verify_user(
            url_path = request.host_url,
            username = data.get("username"),
            token = data.get("token")
        ):
            return jsonify(status = True, message = "Hidden data is `amF5c2U=`")
        return jsonify(status = False, message = "Not hidden data for you c:")


index_page = ServiceView.as_view('index')

api_bp.add_url_rule("/service", view_func=index_page)