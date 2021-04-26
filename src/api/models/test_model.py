from . import db


class TestModel(db.Model):
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True)
    date_stamp = db.Column(db.String(), nullable=False)
    result = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Teste feito em {self.date_stamp}. Resultado {self.result}>'
