from flask import (render_template, flash, redirect, session, url_for, request,
                   g, jsonify, abort)
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)
from flask.ext.socketio import SocketIO, emit
from app import app, db, lm, socketio
from .forms import LoginForm, RegisterForm
from .models import User
from .auth import *
import json
from uuid import uuid4


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.user = current_user


@app.route("/")
@app.route("/index")
def index():
    """Handles calls to / and /index, return the panel"""
    # return render_template(
    #     "index.html",
    #     title="CactusPanel",
    #     form=LoginForm()
    # )
    return oauth_authorize("beam")


@app.route("/authorize/<provider>")
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route("/callback/<provider>")
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    oauth = OAuthSignIn.get_provider(provider)
    # social_id, username, email = oauth.callback()
    print(oauth_callback())
    # if social_id is None:
    #     flash('Authentication failed.')
    #     return redirect(url_for('index'))
    # user = User.query.filter_by(social_id=social_id).first()
    # if not user:
    #     user = User(social_id=social_id, nickname=username, email=email)
    #     db.session.add(user)
    #     db.session.commit()
    # login_user(user, True)
    # return oauth.authorize()


@app.route("/login")
def login():
    return oauth_authorized("beam")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
