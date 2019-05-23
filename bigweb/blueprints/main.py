from flask import Blueprint,render_template,redirect,url_for,request,jsonify
from bigweb.decorate import confirm_required
from flask_login import login_required
from flask_login import current_user
from bigweb.models import User,Role,Permission,Post,Comment
from bigweb.extensions import db
from bigweb.forms import CommentForm

main_bp = Blueprint("main",__name__)


@main_bp.route("/")
def index():
    # db.drop_all()
    # db.create_all()
    posts = reversed(Post.query.all())

    # userr = db.session.execute("""SELECT email FROM user
    #     WHERE email='17640175486@163.com'
    # """).first()
    # print("**********************************")
    # print(userr)

    return render_template("main/index.html",posts=posts)



@main_bp.route("/post/<int:post_id>",methods=["GET","POST"])
def post(post_id):
    comment_form = CommentForm()
    if request.method == "POST":
        print("**********************")
        print(post_id)

        data = request.get_json()
        if data is None or data["comment"].strip() == "":
            return "没有获取数据"
        comment = data["comment"]

        print("******************************************")
        print("获取到了数据")
        print(comment)
        comment_sql = Comment(comment=comment,post_id=post_id,user_id=current_user.id)
        db.session.add(comment_sql)
        db.session.commit()
        return """
                        <div class="comment-list">
                    <div class="comment-list-image"><img src="{{ url_for("user.get_file",filename=comment.post.user.portrait) }}" alt=""></div>
                    <div class="comment-list-body">
                        <div class="comment-list-top">
                            <p class="comment-p"><a href="#">{}👌🌹：</a>{}</p>
                        </div>
                        <div class="comment-list-add">
                            <span class="comment-list-time">{{ comment.timestamp }}</span>
                            <button class="comment-list-reply">回复&nbsp;|&nbsp;👍 点赞</button>
                        </div>
                    </div>
                </div>
        """.format(comment_sql.user.username,comment_sql.comment),200
    post = Post.query.get(post_id)
    return render_template("main/post.html",post=post,comment_form=comment_form)

@main_bp.route("/comment-ajax/<int:post_id>",methods=["POST"])
def comment_ajax(post_id):
    data = request.get_json()
    if data is None or data["comment"].strip() == "":
        return "没有获取数据"
    comment = data["comment"]
    comment_sql = Comment(comment=comment, post_id=post_id, user_id=current_user.id)
    db.session.add(comment_sql)
    db.session.commit()
    return """
                    <div class="comment-list">
                <div class="comment-list-image"><img src="{}" alt=""></div>
                <div class="comment-list-body">
                    <div class="comment-list-top">
                        <p class="comment-p"><a href="#">{}👌🌹：</a>{}</p>
                    </div>
                    <div class="comment-list-add">
                        <span class="comment-list-time">{}</span>
                        <button class="comment-list-reply">回复&nbsp;|&nbsp;👍 点赞</button>
                    </div>
                </div>
            </div>
    """.format(url_for("user.get_file",filename=comment_sql.post.user.portrait),comment_sql.user.username, comment_sql.comment, comment_sql.timestamp), 200

