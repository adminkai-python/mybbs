from flask import Flask
from bigweb.settings import config
import os
from bigweb.settings import config

def create_app(config_name=os.getenv("FLASK_ENV")):
    app = Flask("bigweb")
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    # app.config["CKEDITOR_FILE_UPLOADER"] = "user.upload"


    return app



from bigweb.blueprints.main import main_bp
from bigweb.blueprints.user import user_bp
from bigweb.blueprints.auth import auth_bp
# from bigweb.blueprints.admin import admin_bp
from bigweb.extensions import db,login,mail,ckeditor,moment,dropzone
from bigweb.apis.v1.main import api_v1_main


# 注册蓝本函数
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    # app.register_blueprint(admin_bp)
    app.register_blueprint(api_v1_main)


# 注册扩展函数
def register_extensions(app):
    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    dropzone.init_app(app)


# 注册日志函数
# 注册钩子函数
# 注册自定义命令函数
# 注册错误页面函数