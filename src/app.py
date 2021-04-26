from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from environs import Env
from os import getenv
from emoji import emojize

from src.config.config import config_selector
from src.config import database
from src.config import commands
from src.api import views

env = Env()
env.read_env()

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Status Covid API"
    }, )


def create_app():
    app = Flask(__name__)

    config_type = getenv("FLASK_ENV")

    app.config.from_object(config_selector[config_type])

    database.init_app(app)

    commands.init_app(app)

    views.init_app(app)

    print(emojize('Online :fire:'))

    app.register_blueprint(swaggerui_blueprint)

    return app
