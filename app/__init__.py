import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'somerandomsecretkey'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''

    app.config['ADMINS'] = ['']
    db.init_app(app=app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.login'

    from app.accounts.views import accounts_blueprint
    app.register_blueprint(accounts_blueprint, url_prefix="/accounts")

    from app.investments.views import investments_blueprint
    app.register_blueprint(investments_blueprint, url_prefix="/investments")

    from app.graphs.views import graphs_blueprint
    app.register_blueprint(graphs_blueprint, url_prefix="/graphs")

    # from TheCryptoSense.accounts.routes import auth
    # app.register_blueprint(auth)

    return app

from app import models
