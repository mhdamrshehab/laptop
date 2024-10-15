from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from app.models.User import User
from app import db
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
   return render_template('index.html')

@main.route('/login',methods=['Get','POST'])
def create():
   return render_template('Auth/login.html')

@main.route('/auth',methods=['GET','POST'])
def login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      if (User.check_credentials(email, password)==1):
         flash('Logged in successfully!', 'success')
         return redirect(url_for('main.index'))
      elif (User.check_credentials(email, password)==0):
         print ("Admin")
      else:
         return render_template('Auth/login.html', message='Invalid credentials')
   return render_template('Auth/login.html', message='Invalid credentials')
   
   

@main.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered, please use another one.', 'error')
            return redirect(url_for('main.register'))

        # Create new user and hash the password
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            username=username,
            password=hashed_password,
            phone=phone
        )

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        except:
            db.session.rollback()
            flash('Error during registration. Please try again.', 'error')
    
    return render_template('Auth/register.html')





