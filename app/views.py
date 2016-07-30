"""All the views for the site."""

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
    """Load a user, and return it."""
    return User.get(id=user_id)


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user."""
    g.rdb_conn = rethink.connect(host=app.config["RDB_HOST"],
                                 port=app.config["RDB_PORT"],
                                 db=app.config["RDB_DB"])
    g.user = current_user
    # session["username"] = "DevyMcDevacus"   # For offline debugging


# Error pages
@app.errorhandler(400)
def bad_req(error):
    """Error."""
    return render_template("errors/error.html", error=error)


@app.errorhandler(401)
def not_authorized(error):
    """Error."""
    return render_template("errors/error.html", error=error)


@app.errorhandler(403)
def forbidden(error):
    """Error."""
    return render_template("errors/error.html", error=error)


@app.errorhandler(404)
def page_not_found(error):
    """Error."""
    return render_template("errors/error.html", error=error)


@app.errorhandler(500)
def internal_error(error):
    """Error."""
    return render_template("errors/error.html", error=error)


@app.errorhandler(501)
def not_implemented(error):
    """Error."""
    return render_template("errors/error.html", error=error)


@app.errorhandler(503)
def timeout(error):
    """Error."""
    return render_template("errors/error.html", error=error)


@app.route("/")
@app.route("/index")
def index():
    """Main page."""
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
    """Authorize using oauth from the provided provider."""
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route("/callback/<provider>")
def oauth_callback(provider):
    """Callback for the provided provider."""

    oauth = OAuthSignIn.get_provider(provider)
    oauth_data = oauth.callback()

    oauth_id = oauth_data.get("id", None)
    oauth_username = oauth_data.get("username", None)

    # Are either of these from the OAuth data None?
    if oauth_id is None or oauth_username is None:
        # One is, can't continue with registration
        # TODO: Add proper error handling & make error show up on other tab
        #       with error info, don't just redirect
        flash("OAuth Authentication failed :( Please try again later!")
        return redirect(url_for("index"))

    if not current_user.is_anonymous:
        cur_user = User.get(provider_id="{}${}".format(provider, oauth_id))
        # Bot already exists for user
        if not Bot.get(owner=cur_user):
            # Redirect to index
            return render_template("registration.html", exists=True)

    # Made it this far, user is NOT logged in yet
    # Continue on, let's check if user exists yet or not
    user = User.get(provider_id="{}${}".format(provider, oauth_id))

    if not user:
        # User doesn't exist yet, so we'll create it, then redirect to index
        registered, errors = register(oauth_data)
        if registered:
            # Registration was successful
            # Will tell to close OAuth tab & continue to next step on bot
            #   creation tab
            session["user_id"] = oauth_id
            session["username"] = oauth_username
            session["email"] = oauth_data["email"]
            return render_template("registration.html", errors=None)
        else:
            # Return error to the user
            return render_template("registration.html", errors=errors)


@app.route("/login")
def login():
    """Login route."""

    return oauth_authorize("beam")


@app.route("/logout", methods=["GET"])
def logout():
    """Logout route."""

    logout_user()
    return redirect(url_for("index"))


@app.route("/commands")
def commands_route():
    """Commands route."""

    return render_template("partials/Commands.html")


@app.route("/quotes")
def quotes_route():
    """Quotes route."""

    return render_template("partials/Quotes.html")


@app.route("/dash")
def dashboard_route():
    """Dashboard route."""

    return render_template("partials/Dashboard.html")


@app.route("/goals")
def goals_route():
    """Goals route."""

    return render_template("partials/Goals.html")


@app.route("/messages")
def messages_route():
    """Messages route."""

    return render_template("partials/Messages.html")


@app.route("/repeats")
def repeat_route():
    """Repeat route."""

    return render_template("partials/Repeats.html")


@app.route("/create")
def create(**kwargs):
    """Create route."""
    if current_user.is_anonymous:
        # They're not OAuth logged in, redirect to bot creation
        return render_template("create.html", shouldShow=True)

    # We're here because user IS OAuth Authed
    return render_template("create.html",
                           shouldShow=True,
                           )


@app.route("/create/popup")
def create_popup():
    """Popout route."""
    return render_template("partials/popups/register.html")


@app.route("/support")
def support_route():
    return render_template("partials/Support.html")


@app.route("/ticket/new", methods=["POST"])
def create_ticket():
    """Create a ticket."""
    return render_template("partials/popups/CreateTicket.html")


@app.route("/ticket/respond")
def respond_ticket():
    """Respond to a ticket."""
    return render_template("partials/popups/RespondTicket.html")


@app.route("/goal/new")
def create_goal():
    """Create a goal."""
    return render_template("partials/popups/CreateGoal.html")


@app.route("/command/new")
def make_command():
    """Create a command."""
    return render_template("partials/popups/CreateCommand.html")


@app.route("/command/remove")
def remove_command():
    """Remove a command."""
    return render_template("partials/popups/DeleteCommand.html")
