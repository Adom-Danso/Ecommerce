from . import db
from flask_login import UserMixin, current_user
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import uuid


#=============User table==================
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(120), nullable=False)
	last_name = db.Column(db.String(120), nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	cart = db.relationship('Cart', backref='user', lazy=True)
	wish_list = db.relationship('WishList', backref='user', lazy=True)
	orders = db.relationship('Orders', backref='user', lazy=True)
	role = db.Column(db.String(50), nullable=False, default='normal')
	phone = db.Column(db.String(120), nullable=True)
	address = db.Column(db.String(120), nullable=True)
	address2 = db.Column(db.String(120), nullable=True)
	city = db.Column(db.String(120), nullable=True)
	zip_code = db.Column(db.String(120), nullable=True)
	country = db.Column(db.String(120), nullable=True)

	def __repr__(self):
		return '<User %r>' % self.first_name

	#===========User method for converting the user password in to a hash password===========
	def set_password(self, password):
		hash_password = generate_password_hash(password)
		self.password = hash_password

	#===========Verifying password typed by user when logging in by comparing it to the already stored password===========
	def verify_password(self, password):
		return check_password_hash(self.password, password)

#=============Product table==================
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(50), nullable=False)
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
	image_name = db.Column(db.String(), nullable=False)


#=============Cart table==================
class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


#=============Wishlist table==================
class WishList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


#=============Orders table==================
class Orders(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	username = db.Column(db.String(50), nullable=False)
	order_name = db.Column(db.String(50), nullable=False)
	order_items = db.Column(db.String(200), nullable=False)
	status = db.Column(db.String(50), nullable=False, default='pending')
	delivery_details = db.Column(db.String(50), nullable=False)
	total_price = db.Column(db.Integer, nullable=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	#==============Method for generating unique order names==================
	def generate_order_name(self):
		self.order_name = f"ORDER-{current_user.id}{uuid.uuid4().hex[:10].upper()}"
