from flask import Flask
from flask_login import LoginManager
from . import models
from .config import Configuration
from .models import db
from .main import main
from .admin import admin


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(Configuration)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id.isdigit():
            user_id = int(user_id)
            return models.User.query.filter(models.User.id == user_id).first()
        else:
            return None
    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app
