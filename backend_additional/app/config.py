import os
from flask import url_for

base_dir = os.path.dirname(os.path.abspath(__file__))

class Config:

    DEBUG = False
    LOCAL = False
    APP_PREFIX = '/backend_additional'
    SECRET_KEY = "TEST_SUPER_KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEST_WORD = "THIS IS DEV CONFIG?"
    EXPLAIN_TEMPLATE_LOADING = False
    LOG_DIR = os.path.join(base_dir, 'logs')
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_reset_on_return": "rollback",
    }
    
    def __init__(self) -> None:
        self.SQLALCHEMY_DATABASE_URI = self.get_database_uri(local = self.LOCAL)

    def get_database_uri(self, local = False):
        if not local:
            DB_HOST = os.environ.get("POSTGRES_HOST")
            DB_USER = os.environ.get("POSTGRES_USER")
            DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
            DB_NAME = os.environ.get("POSTGRES_DB")
            prefix = "postgresql+psycopg2://"
            body = f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5433/{DB_NAME}"
            uri = f"{prefix}{body}"
        else:
            uri = "postgresql+psycopg2://jayse_test:test@localhost:5433/test_db_add"
        return uri

class DevConfig(Config):
    """ DevConfig """

class TestConfig(Config):

    LOCAL = True
    TEST_WORD = "THIS IS TEST CONFIG?"
    DEBUG = True

    def __init__(self) -> None:
        super().__init__()
