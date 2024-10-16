from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from app.models.User import User
from app import db
from werkzeug.security import generate_password_hash
from app.models.Product import Product
from werkzeug.utils import secure_filename
import os


main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'email' in session:
        user = User.getUserByEmail(session['email'])
        return render_template('index.html', user=user)
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
         session['email']= email
         session['isAdmin']=0
         return redirect(url_for('main.index'))
      elif (User.check_credentials(email, password)==0):
            session['email']= email
            session['isAdmin']=1
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
      else:
          flash('Invalid email or password', 'error')
          return redirect(url_for('main.login'))
      
   return render_template('Auth/login.html')
      
@main.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('email', None)
    flash('You logged out successfully', 'success')
    return redirect(url_for('main.login'))     

@main.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        image = request.files.get('image')
        image_filename = None
        
        if image:
            image_filename = secure_filename(image.filename)
            uploads_dir = os.path.join(current_app.root_path, '../static/uploads/users')
            
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            image_path = os.path.join(uploads_dir, image_filename)         
            image.save(image_path)
        
        if User.checkExistingUser(email,username):
            flash('Email or username already exists', 'error')
            return redirect(url_for('main.register'))            
        
        if User.pass_confirmed(not password,confirm_password):
            flash('Password and confirm password not matched', 'error')
            return redirect(url_for('main.register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            username=username,
            password=hashed_password,
            phone=phone,
            image=image_filename
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        except:
            db.session.rollback()
            flash('Error during registration. Please try again.', 'error')
    
    return render_template('Auth/register.html')


@main.route('/dashbaord', methods=['GET', 'POST'])
def dashboard():
    if 'email' in session:
        user = User.getUserByEmail(session['email'])
        products = Product.query.all()
        return render_template('admin/dashboard.html',products=products, user=user)
    return redirect(url_for('main.login'))
    

@main.route('/product/<int:id>', methods=['GET'])
def show_product(id):
    product = Product.query.get(id)
    return render_template('admin/products/show.html', product=product)

@main.route('/product/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    print('hello form edit')

@main.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    print('hello from delete')
 
@main.route('/product/create')
def create_product():
      return render_template('admin/products/create.html')

import os

@main.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        color = request.form.get('color')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        offer_price = request.form.get('offer_price')
        model = request.form.get('model')
        brand = request.form.get('brand')

        image = request.files.get('image')
        image_filename = None
        
        if image:
            image_filename = secure_filename(image.filename)
            uploads_dir = os.path.join(current_app.root_path, '../static/uploads/products')
            
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            image_path = os.path.join(uploads_dir, image_filename)         
            image.save(image_path)
        
        new_product = Product(
            title=title,
            description=description,
            category=category,
            color=color,
            quantity=quantity,
            image=image_filename,
            price=price,
            offer_price=offer_price,
            model=model,
            brand=brand
        )

        try:
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except:
            db.session.rollback()
            flash('Error adding product. Please try again.', 'error')

    return render_template('admin/products/create.html')
