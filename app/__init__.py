from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.socketio import SocketIO
from flask.ext.wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth
import eventlet
import json
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
csrf_protect = CsrfProtect(app)
socketio = SocketIO(app)
eventlet.monkey_patch()

from app import views, models
