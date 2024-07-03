from flask import Blueprint, render_template, flash, url_for, redirect
from .forms import NewProduct
from .models import Product, Cart, User
from . import db
from flask_login import current_user, login_required

views = Blueprint('views', __name__)

@views.route('/')
def home():
	products = db.session.execute(db.select(Product)).scalars()
	return render_template('views/home.html', products=products)

@views.route('/food-and-grocery')
def food_and_Grocery():
	products = db.session.execute(db.select(Product).where(Product.food_and_Grocery == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/mobile-phone-and-tablets')
def mobile_phones_and_Tablets():
	products = db.session.execute(db.select(Product).where(Product.mobilePhones_and_Tablets == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/electronics')
def electronics():
	products = db.session.execute(db.select(Product).where(Product.electronics == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/sports')
def sports():
	products = db.session.execute(db.select(Product).where(Product.sports == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/home-furniture-and-appliances')
def home_furniture_and_appliances():
	products = db.session.execute(db.select(Product).where(Product.home_Furniture_and_Appliances == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/fashion')
def fashion():
	products = db.session.execute(db.select(Product).where(Product.fashion == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/health-and-beauty')
def health_and_Beauty():
	products = db.session.execute(db.select(Product).where(Product.health_and_Beauty == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/toys')
def toys():
	products = db.session.execute(db.select(Product).where(Product.toys == '1')).scalars()
	return render_template('views/home.html', products=products)

@views.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
	form = NewProduct()
	if form.validate_on_submit():
		new_product = Product(name=form.name.data, seller=form.seller.data, price=form.price.data, food_and_Grocery=bool(form.food_and_Grocery.data), mobilePhones_and_Tablets=bool(form.mobilePhones_and_Tablets.data), electronics=bool(form.electronics.data), sports=bool(form.sports.data), home_Furniture_and_Appliances=bool(form.home_Furniture_and_Appliances.data), fashion=bool(form.fashion.data), health_and_Beauty=bool(form.health_and_Beauty.data), toys=bool(form.toys.data))
		print(bool(form.food_and_Grocery.data))
		print(bool(form.mobilePhones_and_Tablets.data))
		print(bool(form.electronics.data))
		print(bool(form.sports.data))
		print(bool(form.home_Furniture_and_Appliances.data))
		print(bool(form.fashion.data))
		print(bool(form.health_and_Beauty.data))
		print(bool(form.toys.data))
		db.session.add(new_product)
		db.session.commit()
		return redirect(url_for('views.home'))
	return render_template('views/add_product.html', form=form)


@views.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
	new_item = Cart(product=product_id, user_id=1)
	db.session.add(new_item)
	db.session.commit()
	return redirect(url_for('views.home'))