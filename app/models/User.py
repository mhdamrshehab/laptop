from app import db
from datetime import datetime
from werkzeug.security import check_password_hash

# Initilaztion of the user_product with relation between the product table and user table by thier ids
user_product = db.Table('user_product',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False),
    db.Column('purchase_date', db.DateTime, default=db.func.current_timestamp()),
)

class User(db.Model):
    # Initilaize the table columns
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(15),nullable= False)
    is_admin = db.Column(db.Boolean, default=False)
    image= db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    products = db.relationship('Product', secondary=user_product, back_populates='users') # create relation with Product table.

    # Parameteraized constractar to initialize the object's properities
    def __init__(self, name, phone, email,username,password,isAdmin=False,image=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.username = username
        self.password = password
        self.is_admin = isAdmin
        self.image = image

    # function that check for credentails when user try to log in to the website
    def check_credentials(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            if user.is_admin:
                return 0
            return 1
        return -1
    
    # Function that check if the user is exist in the database using its email or username
    def checkExistingUser(email,username):
        email = User.query.filter_by(email=email).first()
        username=User.query.filter_by(username=username).first()
        if email or username:
            return True
        return False
    
    # Function that user edit its email or username or not.
    def checkEditProfile(id,email,username):
        user=User.getUserById(id)
        if user.email == email and user.username == username:
            email = User.query.filter_by(email=email).first()
            username=User.query.filter_by(username=username).first()
            if email or username:
                return True
            return False
        return False
    
    #  Function to user by its email
    def getUserByEmail(email):
        user = User.query.filter_by(email=email).first()
        return user

    #  Function to user by its id
    def getUserById(id):
        user = User.query.filter_by(id=id).first()
        return user

