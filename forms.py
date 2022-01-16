from typing_extensions import Required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FileField, SelectField, DecimalField, RadioField
from wtforms.validators import DataRequired, Email, Length, Optional, ROUND_UP, InputRequired
from flask_wtf.file import FileRequired

class AddUserForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UploadForm(FlaskForm):
    """Form for Uploading Sounds"""

    audiofile = FileField(validators=[FileRequired()])
    name = StringField('Sound Name', validators=[DataRequired()])
    genre = SelectField('Genre', 
    choices=[('electronic', 'Electronic'), ('classical', 'Classical'), ('pop', 'Pop'), ('experimental', 'Experimental'), 
    ('hiphop', 'HipHop'), ('rap', 'Rap'), ('rock', 'Rock'), ('other', 'Other')], validators=[InputRequired()])
    bpm = DecimalField('bpm', places=2, rounding=ROUND_UP, validators=[InputRequired()])
    sound_type = RadioField('Type', 
    choices=[('piano', 'Piano'), ('guitar', 'Guitar'), ('synth', 'Synth'), ('brass', 'Brass'), ('string', 'String'), 
    ('drums', 'Drums'), ('foley', 'Foley'), ('vocals', 'Vocals')], validators=[InputRequired()] )
    description = TextAreaField('Sound Description', validators=[Length(240), Optional()])

    