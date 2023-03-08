from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Define new db
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # Initialize app within file (hence __name__)
    app = Flask(__name__)

    # Encrypt and secure cookies and session data
    app.config['SECRET_KEY'] = 'l930jlksdflmclsfjIJWLKdfmadflk'

    # Store db in website folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database.db'

    # Initialize db w/ db
    db.init_app(app)

    # Call blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Make sure that models file is initiated
    from .models import User, Note
    with app.app_context():
        db.create_all()

    # init login manager
    login_manager = LoginManager()

    # Redirect if not logged in
    login_manager.login_view = 'auth.login'

    # Start login manager w/ app
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Look for primary key
        return User.query.get(int(id))


    return app

