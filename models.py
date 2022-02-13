"""SQLAlchemy Models for Sample Seeker"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()


   
class Sound(db.Model):
    """Class for Individual Sounds"""

    __tablename__ = 'sounds'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    audiofile = db.Column(
        db.LargeBinary,
        nullable=False
    )

    sound_name = db.Column(
        db.String(40),
        nullable=False
    )

    genre = db.Column(
       db.String,
       nullable=False
    )

    bpm = db.Column(
         db.Float,
        nullable=False
    )

    sound_type = db.Column(
       db.String,
       nullable=False
    )


    description = db.Column(
        db.String(240),
        nullable=False
    )

    # established relationship between Sound and Upload
    uploader= db.relationship('Upload',
                                  backref='sound',
                                  uselist=False)


    def __repr__(self):
        return f"<User #{self.id}:{self.sound_type}, {self.tags}, {self.description}>"


class User(UserMixin, db.Model):
    """User in the Sample Seeker Database"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    password = db.Column(
        db.String,
        nullable=False
    )

    # Est. Relantionship to sounds through our uploads table
    user_uploads = db.relationship('Sound',
                               secondary='uploads',
                               backref='users')

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Upload(db.Model):
    """M2M Model linking users to their uploaded sounds"""

    __tablename__ = 'uploads'

    # Using a Composite Primary Key as this as Associative Entity table, not directly referenced
    user_id = db.Column(db.Integer,
                       db.ForeignKey('users.id'),
                       primary_key=True)
    sound_id = db.Column(db.Integer,
                          db.ForeignKey('sounds.id'),
                          primary_key=True)

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)
    migrate=Migrate(app,db) #Initializing migrate.


    

