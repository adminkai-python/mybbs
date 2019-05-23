from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf.file import FileAllowed,FileRequired,FileField
from wtforms import ValidationError
from bigweb.models import User
from flask_ckeditor import CKEditorField




class RegisterForm(FlaskForm):
    email = StringField("邮箱",validators=[DataRequired(message="无法接收数据"),Length(1,50,message="邮箱长度过长"),Email(message="邮箱格式错误")])
    username = StringField("用户名",validators=[DataRequired(message="无法接收数据"),Length(1,100,message="用户名长度过长")])
    password = PasswordField("密码",validators=[DataRequired(message="无法接收数据"),Length(6,120,message="密码长度必须在6到20位之间"),EqualTo("password2",message="两次输入的密码不一致")])
    password2 = PasswordField("确认密码",validators=[DataRequired(message="无法接收数据")])

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱已经存在")
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("该用户名已经存在")


class LoginForm(FlaskForm):
    email = StringField("邮箱",validators=[DataRequired(message="无法接收数据"),Length(1,50,message="邮箱长度过长"),Email(message="邮箱格式错误")])
    password = PasswordField("密码",validators=[DataRequired(message="无法接收数据"),Length(6,120,message="密码长度必须在6到20位之间")])
    remember = BooleanField("以后免登陆")

class ForgetPasswordForm(FlaskForm):
    email = StringField("邮箱",validators=[DataRequired(message="无法接收数据"),Length(1,50,message="邮箱长度过长"),Email(message="邮箱格式错误")])


class ResetPasswordForm(FlaskForm):
    email = StringField("邮箱",validators=[DataRequired(message="无法接收数据"),Length(1,50,message="邮箱长度过长"),Email(message="邮箱格式错误")])
    password = PasswordField("密码",validators=[DataRequired(message="无法接收数据"),Length(6,120,message="密码长度必须在6到20位之间"),EqualTo("password2",message="两次输入的密码不一致")])
    password2 = PasswordField("确认密码",validators=[DataRequired(message="无法接收数据")])




class PostForm(FlaskForm):
    title = StringField("",validators=[DataRequired(message="无效数据"),Length(1,290,message="标题过长")],render_kw={"placeholder":"输入标题"})
    article = CKEditorField("",validators=[DataRequired(message="无效数据"),Length(1,2990,message="字数不能超过2990字")])



class PortraitForm(FlaskForm):
    portrait = FileField("",validators=[FileRequired(message="没有图片"),FileAllowed(['jpg','png','jpeg','pneg','gif'],message="图片格式不支持")])


class CommentForm(FlaskForm):
    comment = TextAreaField("",validators=[DataRequired(message="无效数据"),Length(1,1500,message="字数上限1500")])



















