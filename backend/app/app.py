from flask import Flask, session
from flask_cors import CORS
from werkzeug.utils import redirect

from config import TestConfig, DevConfig
from models import db
from auth import init_login
from admin import init_admin, _init_catalogs
from logger_config import init_logger

from blueprints.index.index import index_bp
from blueprints.api.api_local import api_bp
from blueprints.login.login import login_bp
from blueprints.broken_email_reset.reset import reset_bp
from blueprints.broken_query.broken_query import sqli_bp
from blueprints.broken_comments.broken_comments import xss_bp

def create_app():
    
    app = Flask(__name__)
    CORS(app)

    # Init config
    app.config.from_object(DevConfig())

    # Init logger
    init_logger(app)

    # Init database
    db.init_app(app)
    @app.before_first_request
    def create_test_admin():
        db.create_all()
        _init_catalogs(test=False)

    # Register blueprints

    app.register_blueprint(api_bp, url_prefix = app.config.get("APP_PREFIX") + "/api")
    app.register_blueprint(index_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(login_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(reset_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(sqli_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(xss_bp, url_prefix = app.config.get("APP_PREFIX"))
    
    # Init modules
    init_login(app)
    init_admin(app)
    
    return app

def create_test_app():

    app = Flask(__name__)
    CORS(app)

    # Init config
    app.config.from_object(TestConfig())

    # Init logger
    init_logger(app)

    # Init database
    db.init_app(app)
    @app.before_first_request
    def create_test_admin():
        # db.drop_all()
        db.create_all()
        _init_catalogs(test=True)

    # Register blueprints
    
    app.register_blueprint(api_bp, url_prefix = app.config.get("APP_PREFIX") + "/api")
    app.register_blueprint(index_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(login_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(reset_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(sqli_bp, url_prefix = app.config.get("APP_PREFIX"))
    app.register_blueprint(xss_bp, url_prefix = app.config.get("APP_PREFIX"))

    # Init modules
    init_login(app)
    init_admin(app)

    return app