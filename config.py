import os
from flask.cli import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY for repository'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'develop.sqlite3.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_KEY = os.environ.get('GOOGLE_KEY') or 'GOOGLE_KEY'
