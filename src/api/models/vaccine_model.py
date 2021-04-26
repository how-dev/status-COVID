from . import db


class VaccineModel(db.Model):
    __tablename__ = "vaccines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    record = db.Column(db.String, nullable=False)
    voucher = db.Column(db.String, nullable=False)  # Foto vai ser a url, por enquanto
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=True)
