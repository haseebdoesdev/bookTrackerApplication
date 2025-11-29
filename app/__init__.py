import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Determine if running in development mode
    flask_env = os.environ.get('FLASK_ENV', 'development')
    flask_debug = os.environ.get('FLASK_DEBUG', '0')
    is_development = flask_env == 'development' or flask_debug == '1'
    
    # Configure the app
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        if is_development:
            secret_key = 'dev-fallback-key-change-in-production'
            import warnings
            warnings.warn("Using development SECRET_KEY. Set SECRET_KEY environment variable for production!")
        else:
            raise ValueError("SECRET_KEY environment variable must be set in production!")
    
    app.config['SECRET_KEY'] = secret_key
    
    # Database configuration with fallback for development
    database_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
    if not database_uri:
        if is_development:
            # Use SQLite for development if no database URI is set
            database_uri = 'sqlite:///booktracker.db'
            import warnings
            warnings.warn("Using SQLite development database. Set SQLALCHEMY_DATABASE_URI for production!")
        else:
            raise ValueError("SQLALCHEMY_DATABASE_URI environment variable must be set in production!")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.books import books_bp
    from app.routes.challenges import challenges_bp
    from app.routes.profile import profile_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(profile_bp)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app 