from app import db

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
        
    
    
    