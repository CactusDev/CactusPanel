from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.socketio import SocketIO
from flask.ext.wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth
import eventlet
import json
from os.path import abspath, join, dirname

app = Flask(__name__)
config = json.load(open(abspath(join(dirname(__file__), "..", "data/config.json"))))
app.config.from_object(config)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
csrf_protect = CsrfProtect(app)
oauth = OAuth()
beam_app = oauth.remote_app(
    "beam",
    base_url="https://beam.pro/api/v1/",
    request_token_url="https://beam.pro/api/v1/oauth/token",
    authorize_url="https://beam.pro/oauth/authorize",
    consumer_key=config["client_id"],
    consumer_secret=config["client_secret"]
)
socketio = SocketIO(app)
eventlet.monkey_patch()

from app import views, models
