from app import db
from flask_security import (
    # Security,
    # MongoEngineUserDatastore,
    UserMixin,
    RoleMixin,
    # auth_required,
    # hash_password,
)


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
