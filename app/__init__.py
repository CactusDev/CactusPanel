from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, request
from flask_socketio import SocketIO
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail
from flask_security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin, login_required,
                            login_user, logout_user, current_user)
from flask_jsglue import JSGlue


app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("config.py", True)

mail = Mail(app)
mail.init_app(app)

db = SQLAlchemy(app)

csrf_protect = CsrfProtect(app)

socketio = SocketIO(app)

jsglue = JSGlue(app)

from .models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

lm = LoginManager()

lm.init_app(app)
lm.login_view = "login"

from . import views, models
from .util import assets

from . import views
