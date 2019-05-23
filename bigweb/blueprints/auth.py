from flask import Blueprint,render_template,redirect,url_for,flash
from bigweb.forms import RegisterForm,LoginForm,ForgetPasswordForm,ResetPasswordForm
from bigweb.models import User
from bigweb.extensions import db
from flask_login import login_user,logout_user,current_user,login_required
from bigweb.utils import generate_token,validate_token
from bigweb.settings import Operation
from bigweb.emails import send_confirm_email,send_password_email


auth_bp = Blueprint("auth",__name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        email = register_form.email.data
        username = register_form.username.data
        password = register_form.password.data


        user = User(email=email, username=username)
        user.set_password(password)


        db.session.add(user)
        db.session.commit()

        token = generate_token(user=user, operation=Operation.CONFIRM)
        send_confirm_email(user=user,token=token)

        flash("已经向您的邮箱发送了一份验证邮件，赶快去验证吧")
        login_user(user)
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", register_form=register_form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data.lower()
        password = login_form.password.data
        remember = login_form.remember.data
        user = User.query.filter_by(email=email).first()
        if user:
            if user.validate_password(password):
                login_user(user,remember)
                return redirect(url_for("main.index"))
            else:
                flash("密码错误，请重新输入")
        else:
            flash("该邮箱没有注册，请先注册")
    return render_template("auth/login.html", login_form=login_form)



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route("/confirm/<token>")
def confirm(token):
    # if not current_user.is_authenticated:
    #     flash("您可以在个人中心进行邮箱验证")
    #     return redirect(url_for("auth.login"))
    if current_user.confirmed == True:
        return redirect(url_for("main.index"))
    if validate_token(user=current_user,token=token,operation=Operation.CONFIRM):
        flash("邮箱验证成功")
        return redirect(url_for("main.index"))
    else:
        flash("邮箱验证失败")
        return redirect(url_for("resend_email",operation=Operation.CONFIRM))



@auth_bp.route("/resend_email/<operation>")
@login_required
def resend_email(operation):
    token = generate_token(user=current_user,operation=operation)
    if operation == Operation.CONFIRM:
        send_confirm_email(user=current_user,token=token)
        flash("验证邮件已经发送，请赶快查收")
        return redirect(url_for("main.index"))
    elif operation == Operation.CHANGE_EMAIL:
        pass
    else:
        pass


@auth_bp.route("/forget-password",methods=["GET","POST"])
def forget_password():
    forgetpassword_form = ForgetPasswordForm()
    if forgetpassword_form.validate_on_submit():
        email = forgetpassword_form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token(user=user,operation=Operation.RESET_PASSWORD)
            send_password_email(user=user,token=token)
            flash("重置密码的验证邮件已经发往你的邮箱，请尽快验证")
            return redirect(url_for("auth.login"))
        flash("这个邮箱地址并没有在网站注册，请重新输入")
        return redirect(url_for("auth.forget_password"))
    return render_template("auth/forget_password.html", forgetpassword_form=forgetpassword_form)



@auth_bp.route("/reset-password/<token>",methods=["GET","POST"])
def reset_password(token):
    resetpassword_form = ResetPasswordForm()
    if resetpassword_form.validate_on_submit():
        email = resetpassword_form.email.data.lower()
        password = resetpassword_form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if validate_token(user=user, token=token, operation=Operation.RESET_PASSWORD):
                user.set_password(password)
                db.session.commit()
                flash("密码设置成功，请您牢记您的密码")
                return redirect(url_for("auth.login"))
            else:
                flash("邮箱验证失败，请重新验证邮箱")
                return redirect(url_for("auth.forget_password"))
        else:
            flash("无效的邮箱，请重新输入")
            return redirect(url_for("auth.reset_password", token=token))
    return render_template("auth/reset_password.html",resetpassword_form=resetpassword_form)






















