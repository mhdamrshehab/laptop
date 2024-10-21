from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import secrets
from datetime import timedelta


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__ ,template_folder='../templates', static_folder='../static')


    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/laptop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.permanent_session_lifetime = timedelta(minutes=60) 
    app.config['SESSION_COOKIE_DURATION'] = timedelta(minutes=60)


    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models import User, Product
    
    from app.routes import main
    app.register_blueprint(main)

    return app
