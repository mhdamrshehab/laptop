from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session,jsonify
from app.models.User import User
from app import db
from werkzeug.security import generate_password_hash
from app.models.Product import Product
from werkzeug.utils import secure_filename
import os


main = Blueprint('main', __name__)

@main.route('/')
def index():
    best_sellers = Product.getBestSellers()
    offers = Product.getOffers()
    newArrivals= Product.getNewArrivals()
    if 'email' in session:
        user = User.getUserByEmail(session['email'])
        return render_template('index.html', user=user, best_sellers=best_sellers , offers=offers, newArrivals= newArrivals)
    return render_template('index.html', best_sellers=best_sellers , offers=offers, newArrivals= newArrivals)

# Auth methods

@main.route('/login',methods=['Get','POST'])
def create():
   return render_template('Auth/login.html')

@main.route('/auth',methods=['GET','POST'])
def login():
   
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
      
      if (User.check_credentials(email, password)==1):
         session.permanent = True 
         session['email']= email
         session['isAdmin']=0
         flash('Logged in successfully!', 'success')
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
    session.pop('isAdmin', None)
    flash('You logged out successfully', 'success')
    return redirect(url_for('main.login'))     

@main.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        if User.checkExistingUser(email,username):
            flash('Email or username already exists', 'error')
            return redirect(url_for('main.register'))            
        
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            username=username,
            password=hashed_password,
            phone=phone,
            image=None
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            
            user_id=new_user.id
            image = request.files.get('image')

            if image:
                image_filename = f"{user_id}_{secure_filename(image.filename)}"
                uploads_dir = os.path.join(current_app.root_path, '../static/uploads/users')
                
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                image_path = os.path.join(uploads_dir, image_filename)         
                image.save(image_path)
                
                new_user.image = image_filename
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
    
# -----------------------------------------------------------------------------

# Product methods CRUD

@main.route('/admin/product/<int:id>', methods=['GET'])
def show_product(id):
    product = Product.getProductById(id)
    return render_template('admin/products/show.html', product=product)


 
@main.route('/product/create')
def create_product():
      return render_template('admin/products/create.html')


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

        new_product = Product(
            title=title,
            description=description,
            category=category,
            color=color,
            quantity=quantity,
            price=price,
            offer_price=offer_price,
            model=model,
            brand=brand,
            image=None

        )
        try:
            db.session.add(new_product)
            db.session.commit()
            
            product_id=new_product.id
            image = request.files.get('image')
            
            if image:
                image_filename = f"{product_id}_{secure_filename(image.filename)}"
                uploads_dir = os.path.join(current_app.root_path, '../static/uploads/products')
                
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                    
                image_path = os.path.join(uploads_dir, image_filename)         
                image.save(image_path)
                
                new_product.image = image_filename
                db.session.commit()  
                
            flash('Product added successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except:
            db.session.rollback()
            flash('Error adding product. Please try again.', 'error')

    return render_template('admin/products/create.html')


@main.route('/product/<int:id>/update', methods=['GET', 'POST'])
def update_product(id):
    product = Product.getProductById(id)
    return render_template('admin/products/update.html', product=product)

@main.route('/product/<int:id>/edit', methods=['POST'])
def edit_product(id):
    if request.method == 'POST':
        product = Product.getProductById(id)
        
        product.title = request.form.get('title')
        product.description = request.form.get('description')
        product.category = request.form.get('category')
        product.color = request.form.get('color')
        product.quantity = request.form.get('quantity')
        product.price = request.form.get('price')
        product.offer_price = request.form.get('offer_price')
        product.model = request.form.get('model')
        product.brand = request.form.get('brand')
        
        try:
            db.session.commit()

            image = request.files.get('image')
            if image:
                image_filename = f"{product.id}_{secure_filename(image.filename)}"
                
                uploads_dir = os.path.join(current_app.root_path, '../static/uploads/products')
                
                if product.image:
                    old_image_path = os.path.join(uploads_dir, product.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                    
                image_path = os.path.join(uploads_dir, image_filename)
                image.save(image_path)
                
                product.image = image_filename
                db.session.commit()
            
            flash('Product updated successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating product: {str(e)}', 'error')
            return render_template('admin/products/update.html', product=product)

    return redirect(url_for('main.dashboard'))
@main.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    try:
        product = Product.getProductById(id)
        if not product:
            flash('Product not found.', 'error')
            return redirect(url_for('main.dashboard'))

        if product.image:
            uploads_dir = os.path.join(current_app.root_path, 'static/uploads/products')
            image_path = os.path.join(uploads_dir, product.image)
            
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(product)
        db.session.commit()

        flash('Product deleted successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))
    
    
# --------------------------------- user routes
@main.route('/about')
def about():
    return render_template('user/about.html')

@main.route('/products')
def showProducts():
    
    page = request.args.get('page', 1, type=int)
    pagination= Product.pagination(page)
    return render_template('user/products/index.html', products=pagination.items, pagination=pagination)

@main.route('/search',methods=['GET'])
def search():
    search_input = request.args.get('search')
    category = request.args.get('category')
    page = request.args.get('page', 1, type=int)
    pagination = Product.searchProduct(search_input,page,category)
    if (pagination.items):
        
        return render_template('user/products/index.html', products=pagination.items, pagination=pagination)
    else:
        flash('No Results Founds', 'error')
        return render_template('user/products/index.html' ,pagination=pagination )
    
@main.route('/product/<int:id>')
def show(id):
    product = Product.getProductById(id)
    if product:
        return render_template('user/products/show.html', product=product)
    else:
        flash('Product not found', 'error')
        return redirect(url_for('main.dashboard'))

@main.route('/product/<int:id>/buy', methods=['POST'])
def buy(id):
    if session.get('email'):
        if Product.buyProduct(id):
            flash('Product bought successfully!', 'success')
            return redirect(url_for('main.showProducts'))
        else:
            flash('Failed to buy product', 'error')
            return redirect(url_for('main.showProducts'))
    else:
        flash ('Log in first then buy your product.', 'error')
        return redirect(url_for('main.login'))

@main.route('/profile')
def showProfile():
    email=session.get('email')
    user = User.getUserByEmail(email)
    return render_template('user/profile.html' ,user=user)


@main.route('/editProfile/<int:id>'  ,methods=['GET','POST'])
def editProfile(id):
    user=User.getUserById(id)
    return render_template('user/editProfile.html',user=user)

@main.route('/update/<int:id>',methods=['POST'])
def updateProfile(id):
    if request.method == 'POST':
        flag = False
        user=User.getUserById(id)
        user.name=request.form.get('name')
        username=request.form.get('username')
        email=request.form.get('email')
            
        user.phone=request.form.get('phone')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        
        if User.checkEditProfile(id,email,username):
            flash('Email or username already exists', 'error')
            return redirect(url_for('main.editProfile',id=id))    
        user.email= email
        user.username=username
        if password != "":
            user.password = hashed_password

        image = request.files.get('image')
        image_filename = None
        
        try:
            db.session.commit()

            image = request.files.get('image')
            if image:
                image_filename = f"{user.id}_{secure_filename(image.filename)}"
                
                uploads_dir = os.path.join(current_app.root_path, '../static/uploads/users')
                
                if user.image:
                    old_image_path = os.path.join(uploads_dir, user.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                    
                image_path = os.path.join(uploads_dir, image_filename)
                image.save(image_path)
                
                user.image = image_filename
                db.session.commit()
            
            flash('User updated successfully!', 'success')
            return redirect(url_for('main.logout'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
            return render_template('/user/editPrfile.html', user=user)

    return redirect(url_for('main.showProfile'))
        
@main.route('/contact')
def contact():
    return render_template('user/contact.html')