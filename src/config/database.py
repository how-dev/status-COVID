from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from emoji import emojize

db = SQLAlchemy()


def init_app(app: Flask):
    from src.api import models
    db.init_app(app)
    print(emojize('Base de dados conectada :outbox_tray:'))

    with app.app_context():
        db.create_all()

    app.db = db
