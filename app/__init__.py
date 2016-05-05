from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.socketio import SocketIO
from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.mail import Mail


app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("config.py", True)

mail = Mail(app)
mail.init_app(app)

db = SQLAlchemy(app)

lm = LoginManager()

lm.init_app(app)
lm.login_view = "login"

csrf_protect = CsrfProtect(app)

socketio = SocketIO(app)


from . import views, models
from .util import assets
from .util.mailer import send_mail

app.jinja_env.globals.update(send_mail=send_mail)
app.jinja_env.globals.update(is_supported=views.got_supported)
app.jinja_env.globals.update(reset_supported=views.reset_supported)
