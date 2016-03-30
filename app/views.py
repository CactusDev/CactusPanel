from flask import (render_template, flash, redirect, session, url_for, request,
                   g, jsonify, abort)
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required)
from flask.ext.socketio import SocketIO, emit
from app import app, db, lm, socketio
# from .forms import LoginForm, RegisterForm
from .models import User, Playlist
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


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
