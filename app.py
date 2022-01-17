import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from forms import LoginForm, UploadForm, RegistrationForm
from models import db, connect_db, User, Sound


import pdb
#instantiating an instance of the LoginManager class
login_manager = LoginManager()

app = Flask(__name__)
#marrying our app with the login manager :3 
login_manager.init_app(app)

# Get DB_URI from environ variable 
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///smplskrredux'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "sssh!1234")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# This uses login manager to query our database and determine if the user is logged on or not
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get_one_or_none(user_id)
    return user


##############################################################################
# Login/Register and Logout


@app.route('/')
def get_home():
    """Retrieve and Render Home Route"""

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login Existing User"""

    # generate form
    # validate on submit
    # do shit with the information from the form
    # redirect

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_new_user():
    """Register New User"""

    # generate form
    # validate on submit
    # do shit with the information from the form
    # redirect

    return render_template('register.html')
