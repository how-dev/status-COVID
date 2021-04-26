from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    document = db.Column(db.String(11), nullable=False, unique=True)
    live_with = db.Column(db.Integer, nullable=False)
    exposed_works = db.Column(db.Boolean, nullable=True)

    tests_list = db.relationship('TestModel', lazy="joined", backref=db.backref('user', lazy="joined"))
    # Mais ideias para os dados que precisamos do usuário...

    password_hash = db.Column(db.String, nullable=True)

    vaccines = db.relationship(
        "VaccineModel",
        backref=db.backref("vaccinated_user", lazy="joined"),
        lazy="joined"
    )

    @property
    def password(self):
        raise TypeError("Password could not be accessed")

    @password.setter
    def password(self, new_password):
        new_password_hash = generate_password_hash(new_password)
        self.password_hash = new_password_hash

    def password_check(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)
