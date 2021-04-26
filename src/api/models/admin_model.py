from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class AdminModel(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

    password_hash = db.Column(db.String, nullable=True)

    @property
    def password(self):
        raise TypeError("Password could not be accessed")

    @password.setter
    def password(self, new_password):
        new_password_hash = generate_password_hash(new_password)
        self.password_hash = new_password_hash

    def password_check(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
