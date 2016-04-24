import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = True
PORT = 8000
HOST = "127.0.0.1"    # 0.0.0.0 for public
SECRET_KEY = "CHANGE_THESE"
OAUTH_CREDENTIALS = {
    "Client Name, currently just beam": {
        "CLIENT_ID": "CHANGE_THESE",
        "CLIENT_SECRET": "CHANGE_THESE"
    }
}
