import os

from flask import Flask, render_template_string
from flask.templating import render_template
from flask_mongoengine import MongoEngine
from flask_security import (
    Security,
    MongoEngineUserDatastore,
    UserMixin,
    RoleMixin,
    auth_required,
    hash_password,
)

# Create app
app = Flask(__name__)
app.config["DEBUG"] = True

# Generate a nice key using secrets.token_urlsafe()
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
)
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT", "146585145368132386173505678016728509634"
)

# MongoDB Config
app.config["MONGODB_DB"] = "mydatabase"
app.config["MONGODB_HOST"] = "localhost"
app.config["MONGODB_PORT"] = 27017

# Create database connection object
db = MongoEngine(app)

# from models.user import User, Role


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)
    permissions = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    fs_uniquifier = db.StringField(max_length=64, unique=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(
            email="test@me.com", password=hash_password("password")
        )


# Views
@app.route("/")
@auth_required()
def home():
    # return render_template_string("Hello {{ current_user.email }}")
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
