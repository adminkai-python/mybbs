from bigweb.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask import current_app





class User(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False,index=True)
    username = db.Column(db.String(100),nullable=False)
    password_hash = db.Column(db.String(100))
    register_time = db.Column(db.DateTime,default=datetime.utcnow)
    confirmed = db.Column(db.Boolean,default=False)
    portrait = db.Column(db.String(100))
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))

    role = db.relationship("Role",back_populates="users")
    posts = db.relationship("Post",back_populates="user")
    comments = db.relationship("Comment",back_populates="user")


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.set_role()

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config["MAIL_USERNAME"]:
                self.role = Role.query.filter_by(name="Administrator").first()
                print(self.role.name)
            else:
                self.role = Role.query.filter_by(name="User").first()
                print(self.role.name)
            db.session.commit()


    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)


role_permission = db.Table("role_permission",
                           db.Column("role_id",db.Integer,db.ForeignKey("role.id")),
                           db.Column("permission_id",db.Integer,db.ForeignKey("permission.id"))
                            )

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)

    users = db.relationship("User",back_populates="role")
    permissions = db.relationship("Permission",secondary="role_permission",back_populates="roles")

    @staticmethod
    def init_role():
        role_permission_map = {
            'Locked': ['FOLLOW', 'COLLECT'],
            'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'],
            'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'],
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER']
        }

        for role_name in role_permission_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in role_permission_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()











class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)

    roles = db.relationship("Role",secondary="role_permission",back_populates="permissions")


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(300))
    article = db.Column(db.Text(3000))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    user = db.relationship("User",back_populates="posts")
    comments = db.relationship("Comment",back_populates="post")

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    comment = db.Column(db.Text(1500))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    post = db.relationship("Post",back_populates="comments")
    user = db.relationship("User",back_populates="comments")











































