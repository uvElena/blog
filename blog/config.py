class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../state/blog.db'
    IMAGE_FOLDER = '../state/images'
