from typing_extensions import Required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SelectField, FloatField, RadioField, EmailField
from wtforms.validators import DataRequired, Length, Optional, InputRequired
from flask_wtf.file import FileAllowed, FileRequired

class RegistrationForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    
class LoginForm(FlaskForm):
    """Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UploadForm(FlaskForm):
    """Form for Uploading Sounds"""

    audiofile = FileField('sound', validators=[
        FileRequired(),
        FileAllowed(['wav', 'mp3'], 'Wav and Mp3 only!')
    ])
    sound_name = StringField('Sound Name', validators=[DataRequired()])
    genre = SelectField('Genre', 
    choices=[('electronic', 'Electronic'), ('classical', 'Classical'), ('pop', 'Pop'), ('experimental', 'Experimental'), 
    ('hiphop', 'HipHop'), ('rap', 'Rap'), ('rock', 'Rock'), ('other', 'Other')], validators=[InputRequired()])
    bpm = FloatField('bpm', validators=[InputRequired()])
    sound_type = RadioField('Type', 
    choices=[('piano', 'Piano'), ('guitar', 'Guitar'), ('synth', 'Synth'), ('brass', 'Brass'), ('string', 'String'), 
    ('drums', 'Drums'), ('foley', 'Foley'), ('vocals', 'Vocals')], validators=[InputRequired()] )
    description = TextAreaField('Sound Description', validators=[Length(240), Optional()])

    