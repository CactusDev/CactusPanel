""" All the views for the site """

from app import app
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    """ Index page view """
    return render_template(
        "index.html",
        username="innectic"
        )


@app.route("/commands")
def commands_route():
    return render_template("partials/Commands.html")


@app.route("/quotes")
def quotes_route():
    return render_template("partials/Commands.html")


@app.route("/dash")
def dashboard_route():
    return render_template("partials/Dashboard.html")
