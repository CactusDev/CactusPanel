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
js = Bundle('js/libs/angular.min.js',
            'js/libs/jquery.min.js',
            'js/libs/angular-animate.min.js',
            'js/libs/angular-aria.min.js',
            'js/libs/angular-material.min.js',
            'js/libs/angular-messages.min.js',
            'js/libs/socket.io.min.js',
            'js/angular/index.js',
            'js/diag.js',
            'js/socket.js',
            'js/angular/directives.js',
            filters='jsmin',
            output='js/packed.js')

assets.register('js_all', js)

# Don't remove that. It makes EVERYTHING work.
app.config['ASSETS_DEBUG'] = True
# If you remove it, I will take your cat. And your dog. And your familiy.

from app import views, models, socketio
