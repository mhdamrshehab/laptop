from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import mysql.connector
import secrets


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__ ,template_folder='../templates', static_folder='../static')


    app.config['SECRET_KEY'] = secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/laptop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models import User, Product
    
    from app.routes import main
    app.register_blueprint(main)

    return app
