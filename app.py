import os

from flask import Flask, render_template_string
from flask.templating import render_template

from flask_security.forms import LoginForm

from flask_security import (
    Security,
    MongoEngineUserDatastore,
    auth_required,
    hash_password,
)


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
# app.config["SECURITY_USER_IDENTITY_ATTRIBUTES"] = ("username", "email")

# below import should be done only after the "app" initialization
from database import db

from models.user.user import User, Role, ExtendedLoginForm

# from models.user.user import User, Role


user_datastore = MongoEngineUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
security = Security(app, user_datastore)
# security = Security(app, user_datastore, login_form=LoginForm)

# a = LoginForm()

# security = Security(app, user_datastore, login_form=ExtendedLoginForm)


@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(
            email="test@me.com", password=hash_password("password")
        )


# @app.route("/login")
# # @auth_required()
# def login_page():
#     return "Podde"


@app.route("/")
@auth_required()
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
