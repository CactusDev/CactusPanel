from flask import (render_template, flash, redirect, url_for, g, jsonify,
                   session)
from flask_login import (request, login_required, current_user, login_user,
                         logout_user)
from . import app, lm
from .forms import LoginForm, RegisterForm
from .auth import OAuthSignIn
from .util import tickets
import json
from uuid import uuid4
import remodel.connection
from rethinkdb.errors import ReqlDriverError
from .rethink_models import *
import rethinkdb as rethink
import sys
import rethinkdb as rethink

remodel.connection.pool.configure(db=app.config["RDB_DB"])


@lm.user_loader
def load_user(user_id):
    return User.get(id=user_id)


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                                 port=app.config["RDB_PORT"],
                                 db=app.config["RDB_DB"])
    g.user = current_user
    # session["username"] = "foo"   # For offline debugging


@app.route("/")
@app.route("/index")
@login_required
def index():
    """Handles calls to / and /index, return the panel"""

    if "username" in session:
        print("Index:CurrentUser:\t", current_user)

        return render_template(
            "index.html",
            form=LoginForm(),
            username=session["username"]
        )
    else:
        # HACK: For whatever reason, Flask thinks users are logged in
        #       and causes a crash, so we're making sure that doesn't happen
        logout_user()
        return redirect(url_for("index"))


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

    user = User.get(provider_id="{}${}".format(provider, user_id))
    print(user)
    if not user:
        # User doesn't exist yet, so we'll create it, then redirect to index
        registered, e = register()
        if registered:
            return redirect(url_for("index"))
        else:
            # TODO: Make this redirect to an error page
            return jsonify({"error": 3, "data": jsonify(e.args)})

    else:
        # User exists, so login and redirect to index
        login_user(user, True)
        return redirect(url_for("index"))


@app.route("/register")
def reg():
    session["user_id"] = "24228"
    session["username"] = "ParadigmShift3d"
    session["email"] = "paradigmshift3d@gmail.com"
    session["provider"] = "beam"
    foo, e = register()


def register():
    # try:
    user_role = UserRole.get_or_create(name="user")
    current_time = rethink.now()
    new_user = User.create(
        userName=session["username"],
        password="",    # None, because it's required for
                        # Flask-Login's auth key setup,
        email=session["email"],
        confirmed_at=current_time,
        roles=[user_role[0]["name"]],
        provider_id="{pid}${uid}".format(pid=session["provider"],
                                         uid=session["user_id"]),
        active=True
    )

    new_user.save()

    user = User.get(provider_id="{}${}".format(
        session["provider"],
        session["user_id"]
    ))

    if user is not None:
        login_user(user, True)
        return True, None
    else:
        return False, None
    # except Exception as e:
    #     return False, e


@app.route("/login")
def login():
    return oauth_authorize("beam")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/admin', methods=["GET"])
@login_required
def admin():
    return render_template('admin.html')


@app.route('/c-emoji', methods=["GET"])
def emoji():
    return render_template('partials/c-emoji.html')


@app.route('/command/create')
def create_command():
    return render_template(
        'partials/AddCommand.html',
        username=session["username"],
        role="pro")


@app.route('/tab/dash')
def dash():
    return render_template(
        'partials/tabs/Dashboard.html',
        username=session["username"],
        role="pro")


@app.route('/tab/commands')
def commands():
    return render_template(
        'partials/tabs/Commands.html',
        username=session["username"],
        role="pro")


@app.route('/tab/botsettings')
def bot_settings():
    return render_template(
        'partials/tabs/BotSettings.html',
        username=session["username"],
        role="pro")


@app.route('/tab/support')
def support():
    return render_template(
        'partials/tabs/Support.html',
        username=session["username"],
        role="pro")


@app.route('/tab/usersettings')
def user_settings():
    return render_template(
        'partials/tabs/UserSettings.html',
        username=session["username"],
        role="pro")
