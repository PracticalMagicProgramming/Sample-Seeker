from distutils.command.upload import upload
import os
from io import BytesIO
from sqlite3 import IntegrityError
from flask import Flask, g, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_wtf.file import FileField
from sqlalchemy import literal
from werkzeug.utils import secure_filename
from sqlalchemy.sql import text
from forms import LoginForm, UploadForm, RegistrationForm
from models import  Upload, User, Sound, db, connect_db

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
    """returns user id from session to validate login"""
    user = text(user_id)
    return User.query.filter_by(id=user).first()

##############################################################################
# Login/Register and Logout


@app.route('/')
def get_home():
    """Retrieve and Render Home Route"""

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def returning_user():
    """Logs in an returning user"""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user:
            User.authenticate(form.username.data, form.password.data)
            login_user(user, remember=True)
            flash(f'Hello, {user.username}!', 'success')
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
            user = User.signup( username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
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
# User Routes

@app.route('/users/profile/<int:user_id>')
@login_required
def get_profile_page(user_id):
    #GRAB THE USER
    user = User.query.get_or_404(user_id)
   
    return render_template('profile.html', user=user)

# Get All sounds for this user profile and display them paginated
@app.route('/users/profile/<int:user_id>/sounds/<int:page_num>')
@login_required
def get_user_sounds(user_id, page_num):
    """get and display the user sounds paginated"""
    #Get user
    user = User.query.get_or_404(user_id)

    #Get Uploads using user id 
    user_uploads = Upload.query.filter_by(user_id == user_id).paginate(per_page=5, page=page_num, error_out=True)
    return render_template('display.html', user=user, user_uploads=user_uploads)

##############################################################################
# Sound Views 

@app.route('/sounds/upload', methods=['GET', 'POST'])
@login_required
def get_upload_page():
    """View Function to Upload a Sound to Sample Seeker"""
    
    form = UploadForm()
    user_id = current_user.get_id()
    user =  User.query.get_or_404(user_id)
    
    if form.validate_on_submit():
            # If file data exists
            if form.audiofile.data:
              # Look in the request dictionary, there should be a key with the uploads name
              audio_data = request.files[form.audiofile.name]
              sound = Sound( 
                #reads the upload into the db
                audiofile = audio_data.read(),
                sound_name = secure_filename(form.sound_name.data),
                genre = form.genre.data,
                bpm = form.bpm.data,
                sound_type = form.sound_type.data,
                description = form.description.data
                )
            db.session.add(sound)
            db.session.commit()
            
            # add the sound to the current users uploads
            user.user_uploads.append(sound)
            db.session.commit()
            return redirect('/sounds/upload')        
    else:
        return render_template('upload.html', form=form)

@app.route('/sounds/detail/<int:sound_id>')
@login_required
def display_sound_detail(sound_id):
    """Grabs and Displays Detailed Info for a Sound Instance"""
    user_id = current_user.get_id()
    user =  User.query.get_or_404(user_id)
    sound = Sound.query.get_or_404(sound_id)
    
    # logic from unpacking the sound from the DB to preview
    sound_data = BytesIO(sound.audiofile)

    return render_template('detail.html', user=user, sound_data=sound_data, sound=sound)