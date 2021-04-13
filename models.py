from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.Text,
                         primary_key=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.Text,
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user with a hashed password and return an instance of the User class"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return User(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Attempt to authenticate the user. Return an instance of the user class on success or false on failure"""
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
