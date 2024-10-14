from flask import Flask
import mysql.connector

def create_app():
    app = Flask(__name__ ,template_folder='../templates')


    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='laptop'
    )
    
    from app.routes import main
    app.register_blueprint(main)

    return app
