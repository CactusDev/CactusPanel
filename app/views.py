from flask import render_template, flash, redirect, url_for, g, jsonify, session
from flask_login import request
from flask_security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin, login_required,
                            login_user, logout_user, current_user)
from . import app, lm, user_datastore
from .forms import LoginForm, RegisterForm
from .models import User
from .auth import OAuthSignIn
from datetime import datetime


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.user = current_user


@app.route("/")
@login_required
def index():
    """Handles calls to / and /index, return the panel"""
    return render_template(
        "index.html",
        title="CactusPanel",
        form=LoginForm(),
        username="Innectic"
    )


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
    user_id, username, email = oauth.callback()
    session["user_id"] = user_id
    session["username"] = username
    session["email"] = email
    session["provider"] = provider

    if user_id is None:
        flash("OAuth Authentication failed :( Please try again later!")
        return redirect(url_for("index"))
    user = User.query.filter_by(provider_id="{}${}".format(provider,
                                                           user_id)).first()
    if not user:
        # User does not exist, so redirect to registration page
        # Include user_id, username, email
        return redirect(url_for("register"))
    else:
        login_user(user, True)
        return redirect(url_for("index"))


@app.route("/admin", methods=["GET"])
@login_required
def admin():
    return "Foo bar"


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Do foo stuff
            user = user_datastore.create_user(
                username=session["username"],
                email=session["email"],
                confirmed_at=datetime.now(),
                roles=["user"],
                provider_id="{}${}".format(session["provider"], session["user_id"]),
                active=True     # Mark them as active so they're logged in
                )

            login_user(user, True)
            return redirect(url_for("index"))

        else:
            print(form.errors)
            return jsonify({"error": 1, "message": form.errors})

    return render_template("register.html",
                           form=form,
                           title="CactusPanel | Register")


@app.route("/login")
def login():
    return oauth_authorize("beam")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
