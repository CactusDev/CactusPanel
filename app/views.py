""" All the views for the site """

from app import app
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    """ Index page view """
    return render_template("index.html")


@app.route("/<name>")
def dashboard(username):
    #POTATO
    pass
