from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.options(db.joinedload(User.role)).get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # Определения связей внутри класса User
    posts = db.relationship('Post', back_populates='author', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='author', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def role_name(self):
        return self.role.name if self.role else None

    def __repr__(self):
        return f'<User {self.username}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    preview_image_url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan", lazy='dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    author = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')
