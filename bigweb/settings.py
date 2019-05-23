import os

class BaseConfig(object):
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = "127.0.0.1:5000"

    CKEDITOR_ENABLE_MARKDOWN = True
    # CKEDITOR_HEIGHT = "300px"
    # CKEDITOR_WIDTH = "400px"
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_FILE_UPLOADER = "user.upload"

    DROPZONE_MAX_FILE_SIZE = 100
    DROPZONE_MAX_FILES = 30
    DROPZONE_ALLOWED_FILE_TYPE = "default"


class DevelopmentConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(
        os.getenv("MYSQL"),
        os.getenv("PYMYSQL"),
        os.getenv("USERNAME"),
        os.getenv("PASSWORD"),
        os.getenv("HOST"),
        os.getenv("PORT"),
        os.getenv("SQLNAME")
    )



    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Wallace", os.getenv("MAIL_USERNAME"))


class TestingConfig(BaseConfig):
    SECRET_KEY = "hello flask"
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/adminkai/study_flakall/photo/testphoto.db'

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = ("Wallace", os.getenv("MAIL_USERNAME"))




class ProductionConfig(BaseConfig):
    pass





config = {
    "development":DevelopmentConfig,
    "testing":TestingConfig,
    "production":ProductionConfig
}



class Operation:
    CONFIRM = "confirm"
    RESET_PASSWORD = "reset-password"
    CHANGE_EMAIL = "change-email"






















