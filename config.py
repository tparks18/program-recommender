# import os

# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#     DATABASE_URL = os.environ.get('DATABASE_URL')
    
#     if DATABASE_URL and 'postgres://' in DATABASE_URL:
#         SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')
#     elif DATABASE_URL:
#         SQLALCHEMY_DATABASE_URI = DATABASE_URL
#     else:
#         SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL and 'postgres://' in DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')
    elif DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
