from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session,jsonify
from app.models.User import User
from app import db
from werkzeug.security import generate_password_hash
from app.models.Product import Product
from werkzeug.utils import secure_filename
import os
import json


main = Blueprint('main', __name__)

# Home page route, displays best sellers, offers, and new arrivals, and checks if the user is logged in
@main.route('/')
def index():
    best_sellers = Product.getBestSellers()
    offers = Product.getOffers()
    newArrivals= Product.getNewArrivals()
    if 'email' in session:
        user = User.getUserByEmail(session['email'])
        return render_template('index.html', user=user, best_sellers=best_sellers , offers=offers, newArrivals= newArrivals)
    return render_template('index.html', best_sellers=best_sellers , offers=offers, newArrivals= newArrivals)

# Function to check if the user is logged in and return their role (user, admin, or not logged in)
def checkIfLoggedin():
    email=session.get('email')
    isAdmin = session.get('isAdmin')
    if (email != "" and isAdmin == 0):
        return "user"
    elif (email != "" and isAdmin == 1):
        return "admin"
    else:
        return "none"

# Route to render the login page
@main.route('/login',methods=['Get','POST'])
def create():
   return render_template('Auth/login.html')

# Route to handle login form submission and authentication
@main.route('/auth',methods=['GET','POST'])
def login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']
    # Check user credentials
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
          return redirect(url_for('main.create'))
   return redirect(url_for('main.create'))
      
# Route to handle user logout by clearing the session
@main.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('email', None)
    session.pop('isAdmin', None)
    flash('You logged out successfully', 'success')
    return redirect(url_for('main.login'))     

# Route to handle user registration, including form submission and image upload
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

# Route to render the admin dashboard; only accessible by admin users
@main.route('/dashbaord', methods=['GET', 'POST'])
def dashboard():
    if (checkIfLoggedin()== 'admin'):
        user = User.getUserByEmail(session['email'])
        products = Product.query.all()
        return render_template('admin/dashboard.html',products=products, user=user)
    elif (checkIfLoggedin()== 'user'):
        flash ('You are not Authorized to open this page', 'error')
        return redirect(url_for('main.index'))
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))
    
# -----------------------  Product CRUD methods  ---------------------------------------------

# Route to display the details of a specific product; accessible only by admin users
@main.route('/admin/product/<int:id>', methods=['GET'])
def show_product(id):
    if (checkIfLoggedin()== 'admin'):
        product = Product.getProductById(id)
        return render_template('admin/products/show.html', product=product)
    elif (checkIfLoggedin()== 'user'):
        flash ('You are not Authorized to open this page', 'error')
        return redirect(url_for('main.index')) 
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))
    
# Route to render the product creation form; accessible only by admin users
@main.route('/product/create')
def create_product():
    if (checkIfLoggedin()== 'admin'):
      return render_template('admin/products/create.html')
    elif (checkIfLoggedin()== 'user'):
        flash ('You are not Authorized to open this page', 'error')
        return redirect(url_for('main.index')) 
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))

# Route to add a new product; accessible only by admin users
@main.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if (checkIfLoggedin()== 'admin'):
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
    elif (checkIfLoggedin()== 'user'):
        flash ('You are not Authorized to open this page', 'error')
        return redirect(url_for('main.index')) 
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))

# Route to update an existing product; accessible only by admin users
@main.route('/product/<int:id>/update', methods=['GET', 'POST'])
def update_product(id):
    if (checkIfLoggedin()== 'admin'):
        product = Product.getProductById(id)
        return render_template('admin/products/update.html', product=product)
    elif (checkIfLoggedin()== 'user'):
        flash ('You are not Authorized to open this page', 'error')
        return redirect(url_for('main.index')) 
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))

@main.route('/product/<int:id>/edit', methods=['POST'])
def edit_product(id):
    if (checkIfLoggedin()== 'admin'):
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
    elif (checkIfLoggedin()== 'user'):
        flash ('You are not Authorized to open this page', 'error')
        return redirect(url_for('main.index')) 
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))

# Route to edit an existing product; accessible only by admin users
@main.route('/product/<int:id>/delete', methods=['POST'])
def delete_product(id):
    if (checkIfLoggedin()== 'admin'):
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
    elif (checkIfLoggedin()== 'user'):
        flash ('You are not Authorized to open this page', 'error')
        return redirect(url_for('main.index')) 
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))
   
# --------------------------------- user routes -----------------------------------

# Route to render the About page
@main.route('/about')
def about():
    return render_template('user/about.html')

# Route to display a paginated list of products
@main.route('/products')
def showProducts():
    page = request.args.get('page', 1, type=int)
    pagination= Product.pagination(page)
    return render_template('user/products/index.html', products=pagination.items, pagination=pagination)

# Route to handle product search and display paginated results
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

# Route to display a specific product by its ID    
@main.route('/product/<int:id>')
def show(id):
    product = Product.getProductById(id)
    if product:
        return render_template('user/products/show.html', product=product)
    else:
        flash('Product not found', 'error')
        return redirect(url_for('main.dashboard'))

# Route to handle the purchase of a product by its ID
@main.route('/product/<int:id>/buy', methods=['POST','GET'])
def buy(id):
    if checkIfLoggedin()=='user':
        if Product.buyProduct(id):
            flash('Product bought successfully!', 'success')
            return redirect(url_for('main.showProducts'))
        else:
            flash('Failed to buy product', 'error')
            return redirect(url_for('main.showProducts'))
    elif checkIfLoggedin()== 'admin':
        flash('You are not authoriezed to buy product.', 'error')
        return redirect(url_for('main.dashboard'))
    else:    
        flash ('Log in first then buy your product.', 'error')
        return redirect(url_for('main.login'))


# ---------------------------------- Profile Information manipulation ---------------------------------

# Route to display the user's profile if logged in
@main.route('/profile')
def showProfile():
    if (checkIfLoggedin()=="user"):
        email=session.get('email')
        user = User.getUserByEmail(email)
        return render_template('user/profile.html' ,user=user)
    elif (checkIfLoggedin()=="admin"):
        return redirect(url_for('main.dashboard'))
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))

# Route to edit the user's profile
@main.route('/editProfile/<int:id>'  ,methods=['GET','POST'])
def editProfile(id):
    if (checkIfLoggedin()=="user"):
        user=User.getUserById(id)
        return render_template('user/editProfile.html',user=user)
    elif (checkIfLoggedin()=="admin"):
        return redirect(url_for('main.dashboard'))
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))

# Route to update the user's profile information
@main.route('/update/<int:id>',methods=['POST'])
def updateProfile(id):
    if (checkIfLoggedin()=="user"):
            if request.method == 'POST':
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

            return redirect(url_for('main.showProfile'))
    elif (checkIfLoggedin()=="admin"):
        return redirect(url_for('main.dashboard'))
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))
        
#------------------------- Contact us Form manipulation -------------------------------------

# Path to the JSON file where contact data will be stored
contact_file = os.path.join(os.path.dirname(__file__), '../data/contact_data.json')

# Route to render the contact page
@main.route('/contact')
def contact():
    return render_template('user/contact.html')

# Function to save contact data to a JSON file
def save_data_to_JSON(data):    
    if not os.path.exists(contact_file):
        with open(contact_file, 'w') as file:
            json.dump([], file)
    
    with open(contact_file, 'r') as file:
        try:
            content = json.load(file)
        except json.JSONDecodeError:
            content = []

    content.append(data)
    
    with open(contact_file, 'w') as file:
        json.dump(content, file, indent=4)
        
# Route to process the contact form submission and save data to JSON.
@main.route('/submit_contact',methods=['POST'])
def submit_contact ():
    if request.method== 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(name,email,message)
        data= {
            'name': name,
            'email':email,
            'message': message
        }
        save_data_to_JSON(data)
        flash ('Contact Form submitted successfully', 'success')
        return redirect(url_for('main.contact'))
        
    flash('Error submitting contact form', 'error')
    return redirect(url_for('main.contact'))

# Route to render the admin contact page with submitted contact form data
@main.route('/admin_contact')
def admin_contact():
    if (checkIfLoggedin()=="admin"):
        if os.path.exists(contact_file):
            with open(contact_file, 'r') as file:
                content = json.load(file)
        else:
            content = []
        return render_template('admin/contact.html' ,content=content)
    elif (checkIfLoggedin()=="user"):
        return redirect(url_for('main.index'))
    else:
        flash('Please login first.', 'error')
        return redirect(url_for('main.login'))

        



        


        
    
            