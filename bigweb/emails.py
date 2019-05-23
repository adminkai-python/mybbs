from flask_mail import Message
from bigweb.extensions import mail
from threading import Thread
from flask import current_app,render_template



def send_email(app,name=None,email=None,token=None,template=None):
    with app.app_context():
        message = Message(subject="confirm email", recipients=[(name,email)])
        message.html = render_template(template,token=token,name=name)
        mail.send(message)

def send_tr_email(user=None,token=None,template=None):
    app = current_app._get_current_object()
    with app.app_context():
        tr = Thread(target=send_email,args=[app,user.username,user.email,token,template])
        tr.start()



def send_confirm_email(user=None,token=None):
    send_tr_email(user=user, template="emails/confirm.html", token=token)

def send_password_email(user,token):
    send_tr_email(user=user,template="emails/reset_password.html",token=token)

def send_change_email(user,token):
    send_tr_email(user=user,template="",token=token)
