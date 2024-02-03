from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main as main_blueprint
    from app.routes.auth import auth as auth_blueprint
    from app.routes.product import product as product_blueprint
    from app.routes.users import users as users_blueprint
    from app.routes.blog import blog as blog_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(blog_blueprint)

    return app
