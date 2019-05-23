from flask import Blueprint,render_template,redirect,url_for,current_app,make_response,flash
from bigweb.models import User,Post,Comment
from bigweb.forms import PostForm,PortraitForm
from flask_login import current_user
from bigweb.extensions import db,ckeditor
from flask import request,send_from_directory
from flask_ckeditor import upload_success,upload_fail
import os
from PIL import Image
from bigweb.utils import random_filename


user_bp = Blueprint("user",__name__)



@user_bp.route("/edit",methods=["GET","POST"])
def post_edit():
    post_form = PostForm()
    if request.method == "POST":
        title = post_form.title.data
        article = post_form.article.data
        post_sql = Post(title=title,article=article,user_id=current_user.id)
        db.session.add(post_sql)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("user/edit.html",post_form=post_form)



@user_bp.route("/get-file",defaults={'filename':'iii.jpg'})
@user_bp.route("/get-file/<filename>")
def get_file(filename):
    path = "/Users/adminkai/study_flakall/photo/bigweb/blueprints/upload"
    if filename is None:
        return send_from_directory("/Users/adminkai/study_flakall/photo/bigweb/static/image","iii.png")
    return send_from_directory(path,filename)


@user_bp.route("/upload",methods=["POST"])
def upload():
    f = request.files.get("upload")
    filename = random_filename(f.filename)

    extension = filename.split(".")[1].lower()
    if extension not in ["jpg","jpeg","gif","png","pneg","jpeg"]:
        return upload_fail(message="格式不支持")

    im = Image.open(f)
    size = im.size
    ima = im
    if size[0]>500:
        ima = im.resize((500,int(size[1]*(500/size[0]))))

    ima.save(os.path.join("/Users/adminkai/study_flakall/photo/bigweb/blueprints/upload",filename))
    url = url_for("user.get_file",filename=filename)
    return upload_success(url=url)




@user_bp.route("/portrait",methods=["GET","POST"])
def set_portrait():
    portrait_form = PortraitForm()
    if portrait_form.validate_on_submit():
        f = portrait_form.portrait.data
        filename = random_filename(f.filename)
        # f = Image.open(f)
        # f = f.resize((48,48))
        current_user.portrait = filename
        db.session.commit()
        f.save(os.path.join("/Users/adminkai/study_flakall/photo/bigweb/blueprints/upload",filename))
        flash("头像上传成功")
        return redirect(url_for("main.index"))
    return render_template("user/self.html",portrait_form=portrait_form)








