from flask import (render_template, flash, redirect, session, url_for, request,
                   g, jsonify, abort)
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)
from flask.ext.socketio import SocketIO, emit
from app import app, db, lm, socketio, beam_app
from .forms import LoginForm, RegisterForm
from .models import User
import json
from uuid import uuid4


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.user = current_user


@app.route("/")
@app.route("/index")
def index():
    """Handles calls to / and /index, return the panel"""
    return render_template(
        "index.html",
        title="CactusPanel",
        form=LoginForm()
    )


@app.route("/oauth_authorized")
@beam_app.authorized_handler
def oauth_authorized(data):
    next_url = request.args.get("next") or url_for("index")

    print(resp)

    if data is None:
        flash(u"OAuth request to authenticate denied")
        return redirect(next_url)

    session["beam_token"] = (
        resp["oauth_token"],
        resp["oauth_token_secret"]
    )

    # flash("You were signed in as {}".format(resp.))
    return redirect(next_url)


@app.route("/login")
def login():
    return beam_app.authorize(
        callback=url_for("oauth_authorized",
        next=request.args.get("next") or request.referrer or None)
    )


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
