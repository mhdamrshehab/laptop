from app import db
from flask import render_template, session
from app.models.User import User 

# Initilaztion of the user_product with relation between the product table and user table by thier ids
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
        
    #  Function to get product by its Id
    def getProductById(id):
        product = Product.query.filter_by(id=id).first()
        return product
    
    #  Function to get best seller products based on the number of times product bought.
    def getBestSellers():
        best_sellers = Product.query.order_by(Product.times_bought.desc()).limit(6).all()
        return best_sellers

    #  Function to get products that have offers.
    def getOffers():
        offers = Product.query.filter(Product.offer_price != None).limit(6).all()
        return offers
    
    #  Function to getnew arrivales products based on the date added to dashboard.
    def getNewArrivals():
        newArrivals = Product.query.order_by(Product.created_at.desc()).limit(6).all()
        return newArrivals
    
    #  Function to get all products.
    def getAllProducts():
        products = Product.query.all()
        return products

    #  Function to search for a product by the search input entered or by the category with the parameter of the page number the user searched in it.
    def searchProduct(search_input, page, category):
        pagination= Product.query.filter(Product.title.like('%' + search_input + '%') | Product.brand.like('%' + search_input + '%') | Product.description.like('%' + search_input + '%') ) 
        if category:
            pagination = pagination.filter_by(category=category)
        pagination = pagination.paginate(page=page, per_page=6)        
        return pagination

    #  Function to paginate the products (each 6 products per page)
    def pagination(page):
        pagination = Product.query.paginate(page=page, per_page=6, error_out=False)
        if pagination.page > pagination.pages and pagination.pages > 0:
            return render_template('errors/no_page.html'), 404
        return pagination

    # Functio to make the buy action the user need to buy based on the product id
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
