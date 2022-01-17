import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

from forms import LoginForm, UploadForm, AddUserForm
from models import db, connect_db, User, Sound


import pdb

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///smplskrredux'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "sssh!1234")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def get_home():
    """Retrieve and Render Home Route"""

    return render_template('index.html')
