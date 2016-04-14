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
app.config["OAUTH_CREDENTIALS"] = {
    "beam": {
        "id": "c38681c3185dadec1c6017dd1e136929f74a091261ed91f7",
        "secret": "e91a674ae4a29b7d3c9dfebfeeb4e18fb30877295f3aa24219239372b68a049e"
    }
}
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
csrf_protect = CsrfProtect(app)
socketio = SocketIO(app)
eventlet.monkey_patch()

from app import views, models
