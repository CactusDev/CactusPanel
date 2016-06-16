from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, request
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("config.py", True)

db = SQLAlchemy(app)

csrf_protect = CsrfProtect(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

from .util import assets
from . import views
