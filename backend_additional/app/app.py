from logging import log
from flask import Flask, session
from flask_cors import CORS
from werkzeug.utils import redirect

from config import TestConfig, DevConfig
from models import db
from logger_config import init_logger

from auth.auth import init_login, test_user_setup
from blueprints.imitation.imitation import imitation_bp
from blueprints.login.login import login_bp

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
        # Create test user
        test_user_setup(app)

    # Register blueprints
    app.register_blueprint(imitation_bp)
    app.register_blueprint(login_bp)

    # Init modules
    init_login(app)

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
        db.drop_all()
        db.create_all()
        # Create test user
        test_user_setup(app)

    # Register blueprints
    app.register_blueprint(imitation_bp)
    app.register_blueprint(login_bp)

    # Init modules
    init_login(app)

    return app