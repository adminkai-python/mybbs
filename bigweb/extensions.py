from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_dropzone import Dropzone


db = SQLAlchemy()
login = LoginManager()
mail = Mail()
ckeditor = CKEditor()
moment = Moment()
dropzone = Dropzone()



@login.user_loader
def load_user(user_id):
    from bigweb.models import User
    user = User.query.get(user_id)
    return user


login.login_view = "auth.login"
login.login_message = "请先登录!"
