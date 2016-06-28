""" Create the flask instance """

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, request
from flask_socketio import SocketIO
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail
from flask_security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin, login_required,
                            login_user, logout_user, current_user)


app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("config.py", True)

csrf = CsrfProtect(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

from . import views
