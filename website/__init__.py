from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    """
    Creates and configures the Flask application.
    Initializes the database, registers blueprints, and sets up login manager.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models
    from .models import User, Measurement

    # Create database tables if they don't exist
    with app.app_context():
        create_database(app)

    # Configure login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        """
        Callback to reload a user object from the user ID stored in the session.
        """
        return User.query.get(int(id))
    
    return app

def create_database(app):
    """
    Creates the database tables if they don't already exist.
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        