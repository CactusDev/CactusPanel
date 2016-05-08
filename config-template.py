import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

SECRET_KEY = "SECRET_KEY"

SECURITY_LOGIN_URL = "/security_login"

OAUTH_CREDENTIALS = {
    "CLIENT_NAME": {
        "CLIENT_ID": "CLIENT_ID",
        "CLIENT_SECRET": "CLIENT_SECRET"
    }
}
