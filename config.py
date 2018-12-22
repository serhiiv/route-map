import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


# """ for local setting, you need to create local_config.py
#     in the local directory with the same list of variables 
# """ 


# # class Config(object):
# try:
#     # local variables
#     from local_config import *

# except ImportError:
#     # devrlop variables

#     SECRET_KEY = 'you-will-never-guess'    
