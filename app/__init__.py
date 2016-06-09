""" Create the flask instance """

from flask import Flask

app = Flask(__name__)
from app import views
