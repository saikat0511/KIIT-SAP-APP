from flask import Flask
import secrets
from pathlib import Path


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

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
