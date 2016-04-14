import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = True
PORT = 8000
SECRET_KEY = "CHANGE_THESE"
client_id = "CHANGE_THESE"
client_secret = "CHANGE_THESE"
