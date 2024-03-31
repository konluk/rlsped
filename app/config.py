import os


class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3308/rlsped'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session management
    SECRET_KEY = os.urandom(24)

    # Flask config
    DEBUG = False

    # User
    USERNAME = "rebeka"
    PASSWORD = "rebeka"


app_config = Config

