import os
from sqlite3 import IntegrityError
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
from forms import LoginForm, UploadForm, RegistrationForm
from models import  db, connect_db, User



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
   
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            login_user(user)
            flash(f'Hello, {user.username}!', 'success')

            # next = request.args.get('next')
            # # is_safe_url should check if the url is safe for redirects.
            # # See http://flask.pocoo.org/snippets/62/ for an example.
            # if not is_safe_url(next):
            #     return os.abort(400)
            
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']
            flash('Invalid credentials.', 'danger')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_new_user():
    """Register New User"""

    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()
            login_user(user)

        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('register.html', form=form)

        return redirect('/')

    else:
        return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')



##############################################################################
# Profile Route

