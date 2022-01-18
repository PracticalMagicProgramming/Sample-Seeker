"""SQLAlchemy Models for Sample Seeker"""
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class Sound(db.Model):
    """Class for Individual Sounds"""

    __tablename__ = 'sounds'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    uploader = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    sound_file = db.Column(
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

    def __repr__(self):
        return f"<User #{self.id}:{self.sound_type}, {self.tags}, {self.description}>"


class User(db.Model):
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

    password = password = db.Column(
        db.String(20),
        nullable=False,
    )

    # maybe make this a join on the condition where this accesses all sounds that have the user id
    # sounds = db.relationship('Sound',
    #                            backref='users')

    
    def __repr__(self):
        return f"<User #{self.id}:{self.fullname}, {self.username}, {self.email}>"

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

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

