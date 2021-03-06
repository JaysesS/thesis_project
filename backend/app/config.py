import os
base_dir = os.path.dirname(os.path.abspath(__file__))

class Config:

    DEBUG = False
    LOCAL = False
    APP_PREFIX = '/backend'
    SECRET_KEY = "DEV_SUPER_KEY"
    JWT_KEY = "DEV_JWT_KEY"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEST_WORD = "THIS IS DEV CONFIG?"
    FLASK_ADMIN_SWATCH = 'superhero'
    FLASK_ADMIN_FLUID_LAYOUT = True
    EXPLAIN_TEMPLATE_LOADING = False
    LOG_DIR = os.path.join(base_dir, 'logs')
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_reset_on_return": "rollback",
    }
    WTF_CSRF_ENABLED = False
    HOST_NAME = "http://thesis.project.com"#os.environ.get("HOST_IP", f"{os.environ.get('APP_HOST')}:5000")
    BACKEND_ADDITIONAL_TOKEN = "904450db12c115c080b9a2a0853ebe7e6af2ced6543c8b9c28e3cfdd"

    # for xss
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = False
    REMEMBER_COOKIE_HTTPONLY = True
    
    def __init__(self) -> None:
        self.SQLALCHEMY_DATABASE_URI = self.get_database_uri(local = self.LOCAL)

    def get_database_uri(self, local = False):
        if not local:
            self.DB_HOST = os.environ.get("POSTGRES_HOST")
            self.DB_USER = os.environ.get("POSTGRES_USER")
            self.DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
            self.DB_NAME = os.environ.get("POSTGRES_DB")
            prefix = "postgresql+psycopg2://"
            body = f"{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:5432/{self.DB_NAME}"
            uri = f"{prefix}{body}"
        else:
            self.DB_HOST = "localhost"
            self.DB_USER = "jayse_test"
            self.DB_PASSWORD = "test"
            self.DB_NAME = "test_db"
            uri = "postgresql+psycopg2://jayse_test:test@localhost:5432/test_db"
        return uri

class DevConfig(Config):
    """ DevConfig """

class TestConfig(Config):

    LOCAL = True
    TEST_WORD = "THIS IS TEST CONFIG?"
    HOST_IP = os.environ.get("HOST_IP", "127.0.0.1:5000")
    DEBUG = True

    def __init__(self) -> None:
        super().__init__()
