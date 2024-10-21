from app import db
from flask import render_template, session
from app.models.User import User 


user_product = db.Table('user_product',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False),
    db.Column('purchase_date', db.DateTime, default=db.func.current_timestamp()),
    extend_existing=True 

)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50))
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255)) 
    price = db.Column(db.Numeric(10, 2), nullable=False)
    offer_price = db.Column(db.Numeric(10, 2))
    model = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    times_bought = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    users = db.relationship('User', secondary='user_product', back_populates='products')

    def __init__(self, title, description, category, color, quantity, image, price, offer_price, model, brand):
        self.title = title
        self.description = description
        self.category = category
        self.color = color
        self.quantity = quantity
        self.image = image
        self.price = price
        self.offer_price = offer_price
        self.model = model
        self.brand = brand
        
    
    def getProductById(id):
        product = Product.query.filter_by(id=id).first()
        return product
    
    def getBestSellers():
        best_sellers = Product.query.order_by(Product.times_bought.desc()).limit(6).all()
        return best_sellers
    
    def getOffers():
        offers = Product.query.filter(Product.offer_price != None).limit(6).all()
        return offers
    
    def getNewArrivals():
        newArrivals = Product.query.order_by(Product.created_at.desc()).limit(6).all()
        return newArrivals
    
    def getAllProducts():
        products = Product.query.all()
        return products
    
    def searchProduct(search_input, page, category):
        pagination= Product.query.filter(Product.title.like('%' + search_input + '%') | Product.brand.like('%' + search_input + '%') | Product.description.like('%' + search_input + '%') ) 
        if category:
            pagination = pagination.filter_by(category=category)
        pagination = pagination.paginate(page=page, per_page=6)        
        return pagination
    
    def pagination(page):
        pagination = Product.query.paginate(page=page, per_page=6, error_out=False)
        if pagination.page > pagination.pages and pagination.pages > 0:
            return render_template('errors/no_page.html'), 404
        return pagination
    
    def buyProduct(product_id):
        user_email = session.get('email')
        user = User.getUserByEmail(user_email) 
        product = Product.query.filter_by(id=product_id).first()
        
        if user and product:
            if product.quantity > 0:
                user_product_entry = user_product.insert().values(
                    user_id=user.id,
                    product_id=product_id,
                    purchase_date=db.func.current_timestamp()
                )
                db.session.execute(user_product_entry)
                product.quantity -= 1
                db.session.commit()
                return True
        return False
