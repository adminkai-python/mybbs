from unittest import TestCase
from bigweb import create_app
from bigweb.extensions import db
from bigweb.models import Role
from flask import url_for


class BaseTestCase(TestCase):

    def setUp(self):
        # 开启程序上下文
        app = create_app("testing")
        self.context = app.test_request_context()
        self.context.push()
        # 生成测试客户端
        self.client = app.test_client()

        # 数据库准备
        db.drop_all()
        db.create_all()
        Role.init_role()





    def tearDown(self):
        db.drop_all()
        self.context.pop()

    def login(self,email=None,password=None):
        if email is None and password is None:
            email = "17640175486@163.com"
            password = "123456"
        return self.client.post(url_for("auth.login"),data={"email":email,"password":password,"remember":True}, follow_redirects=True)


    def register(self, email=None, username=None, password=None, password2=None):
        if email is None and username is None and password is None and password2 is None:
            email = "17640175486@163.com"
            username = "wallace"
            password = "123456"
            password2 = "123456"
        return self.client.post(url_for("auth.register"), data={"email":email, "username":username,  "password":password, "password2":password2}, follow_redirects=True)





