from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), unique=True)
	username = db.Column(db.String(50), unique=True, nullable=True)
	password = db.Column(db.String(120))
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	cart = db.relationship('Cart', backref='user', lazy=True)

	def set_password(self, password):
		hash_password = generate_password_hash(password)
		self.password = hash_password

	def verify_password(self, password):
		return check_password_hash(self.password, password)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	seller = db.Column(db.String(50))
	price = db.Column(db.Integer)
	food_and_Grocery = db.Column(db.Boolean, nullable=True)
	mobilePhones_and_Tablets = db.Column(db.Boolean, nullable=True)
	electronics = db.Column(db.Boolean, nullable=True)
	sports = db.Column(db.Boolean, nullable=True)
	home_Furniture_and_Appliances = db.Column(db.Boolean, nullable=True)
	fashion = db.Column(db.Boolean, nullable=True)
	health_and_Beauty = db.Column(db.Boolean, nullable=True)
	toys = db.Column(db.Boolean, nullable=True)

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

