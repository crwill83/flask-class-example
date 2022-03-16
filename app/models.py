from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

# create our Models based off of our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)
    cart_item = db.relationship('Cart', backref='cart_user', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin=is_admin

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=False)
    image = db.Column(db.String(300))
    caption = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, image, caption, user_id):
        self.title = title
        self.image = image
        self.caption = caption
        self.user_id = user_id

    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False, unique=False)
    image = db.Column(db.String(300))
    description = db.Column(db.String(300))
    price = db.Column(db.Float())
    cart_item = db.relationship('Cart', backref='cart_product', lazy=True)

    def __init__(self, product_name, image, description, price):
        self.product_name = product_name
        self.image = image
        self.description = description
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "image": self.image,
            "description": self.description,
            "price": self.price
        }

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=False)
    image = db.Column(db.String(300))
    ability1 = db.Column(db.String(300))
    ability2 = db.Column(db.String(300))    
    ability3 = db.Column(db.String(300))

    def __init__(self, name, image, ability1, ability2, ability3):
        self.name = name
        self.image = image
        self.ability1 = ability1
        self.ability2 = ability2
        self.ability3 = ability3