from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
# imports for email server setup
from flask_mail import Mail 
import logging
from logging.handlers import SMTPHandler


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
# the mail object used to format and send emails
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    # attaches app to mail object
    mail.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.errors import bp as error_bp
    app.register_blueprint(error_bp)

    from app.settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    from app.history import bp as history_bp
    app.register_blueprint(history_bp, url_prefix='/history')

    from app.media import bp as media_bp
    app.register_blueprint(media_bp, url_prefix='/media')
    
    return app

from app import models