from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import secrets
from pathlib import Path

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    SECRET_FILE_PATH = Path(".flask_secret")
    try:
        with SECRET_FILE_PATH.open("r") as secret_file:
            app.secret_key = secret_file.read()
    except FileNotFoundError:
        # Let's create a cryptographically secure code in that file
        with SECRET_FILE_PATH.open("w") as secret_file:
            app.secret_key = secrets.token_hex(32)
            secret_file.write(app.secret_key)


    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(str(id))

    return app

def create_database(app):
    with app.app_context():
        db.create_all()