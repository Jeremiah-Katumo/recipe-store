
from decouple import config
import os
from dotenv import load_dotenv

basedir = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS= config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(basedir, 'dev.db')
    DEBUG=True
    SQLALCHEMY_ECHO=True   # It helps to see the generated sql commands every time we carry out a database transaction


class ProdConfig(Config):
    pass


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(basedir, 'test.db')
    SQLALCHEMY_ECHO=False   # so that you do not get any sql generated
    TESTING=True


config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}
