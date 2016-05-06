from flask import render_template, flash, redirect, url_for, g, jsonify
from flask.ext.login import (login_user, logout_user, current_user,
                             login_required, request, session)
import json
from . import app, lm, db
from .forms import LoginForm
from .models import User, Tickets
from .auth import OAuthSignIn


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    """Set the Flask session object's user to Flask-Login's current_user"""
    g.user = current_user


@app.route("/")
def index():
    """Handles calls to / and /index, return the panel"""
    return render_template(
        "index.html",
        title="CactusPanel",
        form=LoginForm(),
        username="Innectic",
        role="pro",
        supported=False
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
    user_id, username = oauth.callback()

    if user_id is None:
        flash("OAuth Authentication failed :( Please try again later!")
        return redirect(url_for("index"))
    user = User.query.filter_by(provider_id="{}${}".format(provider,
                                                           user_id)).first()
    if not user:
        # User does not exist, so redirect to registration page
        return redirect(url_for("register"))
    else:
        login_user(user, True)
        return redirect(url_for("index"))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return oauth_authorize("beam")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/admin', methods=["GET"])
def admin():
    return render_template('admin.html')


@app.route('/support/create', methods=["GET", "POST"])
def create_ticket():
    if request.method == "GET":
        return render_template('directives/CreateSupportTicket.html')
    elif request.method == "POST":
        data = json.loads(request.data.decode("utf-8"))

        print(data)
        # new_ticker = Tickets(
        #                 who=request.args["username"],
        #                 issue=request.args["issue"],
        #                 details=request.args["details"]
        #                 )
        # db.session.add(new_ticker)
        # db.session.commit()
        # Support ticket stuff goes here

        return jsonify({"success": True})

        # return redirect(url_for("index", supported=True), code=302)
    else:
        return "Method not supported."


@app.route('/support/respond', methods=["GET", "POST"])
def ticket_response():
    if request.method == "GET":
        return render_template('directives/RespondToTicket.html')
    elif request.method == "POST":
        return "THINGS! #TODO"
    else:
        return "Method not supported."


@app.route('/support/confirmed', methods=["GET"])
def confirmed():
    return render_template('directives/GotSupported.html')


@app.route('/c-emoji', methods=["GET"])
def emoji():
    return render_template('directives/c-emoji.html')


def got_supported():
    if session.get("supported", False) is True:
        return True
    else:
        return False


def reset_supported():
    session["supported"] = None


def do_redirect(where):
    return redirect(where)
