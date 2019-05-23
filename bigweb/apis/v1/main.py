from flask import Blueprint,jsonify
from bigweb import create_app
from bigweb.models import Post


api_v1_main = Blueprint("api_v1_main",__name__)




@api_v1_main.route("/postss",methods=["GET"])
def getposts():
    post = Post.query.first()
    return jsonify({
        "title" : post.title,
        "body" : post.article,
        "timestamp" : post.timestamp
    })





