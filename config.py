import os
from flask.cli import load_dotenv

load_dotenv()

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY for repository'
