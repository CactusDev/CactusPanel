""" All the views for the site """

from flask import (render_template, flash, redirect, url_for, g, jsonify,
                   session)
from flask_login import (request, login_required, current_user, login_user,
                         logout_user)

from . import app, lm
from .auth import OAuthSignIn, register
import json
from uuid import uuid4
import remodel.connection
from rethinkdb.errors import ReqlDriverError
from .models import *
import rethinkdb as rethink
import sys

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
    # session["username"] = "OfflineyMcDevacus"   # For offline debugging


# Error pages

@app.errorhandler(400)
def bad_req(e):
    return render_template("errors/error.html", error=e)


@app.errorhandler(401)
def not_authorized(e):
    return render_template("errors/error.html", error=e)


@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/error.html", error=e)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/error.html", error=e)


@app.errorhandler(500)
def internal_error(e):
    return render_template("errors/error.html", error=e)


@app.errorhandler(501)
def not_implemented(e):
    return render_template("errors/error.html", error=e)


@app.errorhandler(503)
def timeout(e):
    return render_template("errors/error.html", error=e)


@app.route("/")
@app.route("/index")
@login_required
def index():
    """ Index page view """
    if "username" in session:
        print("Index:CurrentUser:\t", current_user)

        return render_template(
            "index.html",
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
    me = oauth.callback()
    session["user_id"] = me.get("id", None)
    session["username"] = me.get("username", None)
    session["email"] = me.get("email", None)
    session["provider"] = provider

    if me.get("id", None) is None or me.get("username", None) is None:
        flash("OAuth Authentication failed :( Please try again later!")
        return redirect(url_for("index"))

    user = User.get(provider_id="{}${}".format(provider, me.get("id", None)))
    print(user)
    if not user:
        # User doesn't exist yet, so we'll create it, then redirect to index
        registered, e = register()
        if registered:
            return redirect(url_for("index"))
        else:
            return render_template("errors/error.html", error=e.args)

    else:
        # User exists, so login and redirect to index
        login_user(user, True)
        return redirect(url_for("index"))


@app.route("/login")
def login():
    return oauth_authorize("beam")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/commands")
def commands_route():
    return render_template("partials/Commands.html")


@app.route("/quotes")
def quotes_route():
    return render_template("partials/Commands.html")


@app.route("/dash")
def dashboard_route():
    return render_template("partials/Dashboard.html")
