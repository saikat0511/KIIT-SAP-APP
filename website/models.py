from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(100))
