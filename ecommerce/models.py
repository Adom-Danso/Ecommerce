from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(120), nullable=False)
	last_name = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(120), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	cart = db.relationship('Cart', backref='user', lazy=True)
	role = db.Column(db.String(50), nullable=False, default='normal')
	phone = db.Column(db.String(120), nullable=True)
	address = db.Column(db.String(120), nullable=True)
	address2 = db.Column(db.String(120), nullable=True)
	city = db.Column(db.String(120), nullable=True)
	zip_code = db.Column(db.String(120), nullable=True)
	country = db.Column(db.String(120), nullable=True)
	
	def set_password(self, password):
		hash_password = generate_password_hash(password)
		self.password = hash_password

	def verify_password(self, password):
		return check_password_hash(self.password, password)

				
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	seller = db.Column(db.String(50))
	price = db.Column(db.Integer, nullable=False)
	food_and_Grocery = db.Column(db.Boolean, nullable=False)
	mobilePhones_and_Tablets = db.Column(db.Boolean, nullable=False)
	electronics = db.Column(db.Boolean, nullable=False)
	sports = db.Column(db.Boolean, nullable=False)
	home_Furniture_and_Appliances = db.Column(db.Boolean, nullable=False)
	fashion = db.Column(db.Boolean, nullable=False)
	health_and_Beauty = db.Column(db.Boolean, nullable=False)
	toys = db.Column(db.Boolean, nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class WishList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
