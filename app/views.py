from flask import (render_template, flash, redirect, url_for, g, jsonify,
                   session)
from flask.ext.login import request
from flask.ext.security import (Security, SQLAlchemyUserDatastore,
                            UserMixin, RoleMixin, login_required,
                            login_user, logout_user, current_user)
from . import app, lm, user_datastore, security, db
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

    print("Index:CurrentUser:\t", current_user)

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
            user_role = user_datastore.find_or_create_role("user")
            user = user_datastore.create_user(
                username=session["username"],
                password="",  # None, because it's required for
                              # Flask-Login's auth key setup
                email=session["email"],
                confirmed_at=datetime.now(),
                roles=[user_role, ],
                provider_id="{pid}${uid}".format(pid=session["provider"],
                                                 uid=session["user_id"]),
                active=True     # Mark them as active so they're logged in
                )

            user = User.query.filter_by(
                provider_id="{}${}".format(session["provider"],
                                           session["user_id"])
                ).first()

            db.session.commit()

            if user is not None:
                login_user(user, True)

                return jsonify({
                    "error": 0,
                    "message": "Registration success!",
                    "redirect": url_for("index")
                    })
            else:
                return jsonify({"error": 2, "message": "User creation failed"})

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
        new_ticker = Tickets(
                        who=data["username"],
                        issue=data["issue"],
                        details=data["details"]
                        )
        db.session.add(new_ticker)
        db.session.commit()
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
