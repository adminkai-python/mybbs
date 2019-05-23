from test.base import BaseTestCase
from flask import url_for
from flask_login import current_user


class MainTestCase(BaseTestCase):

    # 测试首页能否正常访问
    def test_index_page(self):
        response = self.client.get(url_for("main.index"))
        data = response.get_data(as_text=True)
        self.assertIn("注册" and "登录", data)

        self.register()
        self.login()
        response = self.client.get(url_for("main.index"))
        data = response.get_data(as_text=True)
        self.assertIn("发帖" and "注销" and "wallace", data)
        self.assertNotIn("注册" and "登录", data)








        # self.login()
        # response = self.client.get(url_for("main.index"))
        # data = response.get_data(as_text=True)
        # self.assertNotIn("注册", data)
        # self.assertIn("发帖", data)



