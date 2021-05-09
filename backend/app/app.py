from flask import Flask
from flask_cors import CORS

from config import TestConfig, DevConfig
from models import db
from auth import init_login
from admin import init_admin, _init_catalogs
from logger_config import init_logger

from blueprints.bp_test import t_blueprint

def create_app():
    
    app = Flask(__name__)
    CORS(app, resources={r'/*': {"origins": "*"}})

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

    # Init modules
    init_login(app)
    init_admin(app)

    # Register blueprints
    app.register_blueprint(t_blueprint)

    return app

def create_test_app():

    app = Flask(__name__)
    CORS(app, resources={r'/*': {"origins": "*"}})

    # Init config
    app.config.from_object(TestConfig())

    # Init logger
    init_logger(app)

    # Init database
    db.init_app(app)
    @app.before_first_request
    def create_test_admin():
        db.create_all()
        _init_catalogs(test=True)

    # Init modules
    init_login(app)
    init_admin(app)

    # Register blueprints
    app.register_blueprint(t_blueprint)

    return app