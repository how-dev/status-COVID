from os import getenv


class Config:
    JSON_SORTED_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_DEV")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_PRODUCTION")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_TEST")


config_selector = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestConfig
}
