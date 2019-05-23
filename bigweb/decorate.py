from functools import wraps
from flask_login import current_user
from flask  import  redirect,url_for,Markup,flash
from bigweb.settings import Operation


def confirm_required(func):
    @wraps(func)
    def confirm_decorate(*args,**kwargs):
        if not current_user.confirmed:
            message = Markup(
                "您的邮箱还没有验证，请务必先验证邮箱地址"
                "<a class='alert-link' href='{}'>点击这里验证邮箱</a>".format(url_for("auth.resend_email",operation=Operation.CONFIRM))
            )
            flash(message)
            return redirect(url_for("main.index"))
        return func(*args,**kwargs)
    return confirm_decorate
