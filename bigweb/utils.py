from itsdangerous import TimedJSONWebSignatureSerializer as Addhashtool
from itsdangerous import BadSignature,SignatureExpired
from flask import current_app
from bigweb.settings import Operation
from bigweb.extensions import db
import uuid
import os


def generate_token(expire_in=None, user=None, operation=None, **kwargs):
    addhashtool = Addhashtool(current_app.config["SECRET_KEY"], expire_in)
    data = {"id":user.id, "operation":operation}
    data.update(**kwargs)
    return addhashtool.dumps(data)


def validate_token(user,token,operation):
    addhashtool = Addhashtool(current_app.config["SECRET_KEY"])
    try:
        data = addhashtool.loads(token)
    except (BadSignature,SignatureExpired):
        return False
    if user.id != data.get("id") or operation != data.get("operation"):
        return False
    elif operation == Operation.CONFIRM:
        user.confirmed = True
    elif operation == Operation.RESET_PASSWORD:
        return True
    else:
        return False
    db.session.commit()
    return True



def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename



import pymongo

# mongodb数据库操作准备工作
def mongo_connect(database_name="mytest",collection_name=None):
    # 获取数据库服务器
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    # 获取对应的数据库
    database = client[database_name]
    # 获取对应的集合
    collection = database[collection_name]
    return collection




































