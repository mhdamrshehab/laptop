from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Generate a secret key for session management, used for signing cookies to use flash messages
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    # Configure the database URI to connect to MySQL (using PyMySQL driver)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/laptop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set session lifetime to 60 minutes & Configure session cookie expiration to match session lifetime
    app.permanent_session_lifetime = timedelta(minutes=60)
    app.config['SESSION_COOKIE_DURATION'] = timedelta(minutes=60)

    # Initialize the database with the Flask app
    db.init_app(app)
    # Initialize Flask-Migrate with the app and database, enabling migrations
    migrate.init_app(app, db)

    from app.models import User, Product

    from app.routes import main
    app.register_blueprint(main)

    return app
