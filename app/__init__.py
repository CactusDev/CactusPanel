""" Create the flask instance """

from flask import Flask

from flask_login import LoginManager, request
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__, instance_relative_config=True)

app.config.from_object("config")
app.config.from_pyfile("config.py", True)
csrf_protect = CsrfProtect(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

from app import views
