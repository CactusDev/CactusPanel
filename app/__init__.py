from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.socketio import SocketIO
from flask.ext.wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth
from flask.ext.assets import Environment, Bundle

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
assets = Environment(app)
# Does some sort of magical magic. Makes it all one file because #MAGIC™!
js = Bundle(
    'js/libs/jquery.min.js',
    'js/libs/socket.io.min.js',
    'js/diag.js',
    'js/socket.js',
    'js/libs/angular.min.js',
    'js/libs/angular-animate.min.js',
    'js/libs/angular-aria.min.js',
    'js/libs/angular-material.min.js',
    'js/libs/angular-messages.min.js',
    'js/angular/index.js',
    'js/angular/directives.js',
    filters='jsmin',
    output='js/packed.js'
)

assets.register('js_all', js)

# Removed it because it wasn't needed, it kept things js bundler from actually
# bundling stuff
from app import socket
from app import views, models
