from flask import Blueprint, render_template, flash, url_for, redirect, request, current_app as app, abort
from .forms import EditProfile, CheckoutForm, NewProduct
from .models import Product, Cart, User, WishList, Orders
from . import db
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import and_
import secrets, random, json, requests, uuid, os

views = Blueprint('views', __name__)
pay_ref = ''

@views.app_context_processor
def base():
    cart_no = 0
    if current_user.is_authenticated:
	    cart_items = db.session.execute(db.select(Cart).filter(Cart.user_id == current_user.id)).scalars()
	    cart_no = len(list(cart_items))
    return dict(cart_no=cart_no)

@views.route('/')
def home():
    products = list(db.session.execute(db.select(Product)).scalars())
    liked_products = []
    if current_user.is_authenticated:
    	liked_items = db.session.execute(db.select(WishList).filter(WishList.user_id == current_user.id)).scalars()
    	liked_products = [item.product_id for item in liked_items]

    return render_template('views/home.html', products=products, liked_products=liked_products)

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
	if current_user.role == 'admin':
		form = NewProduct()
		print('before validation', flush=True)
		if form.validate_on_submit():
			print('validation success', flush=True)
			new_product = Product(
				name=form.name.data,
				description=form.description.data,
				price=form.price.data,
				food_and_Grocery=form.food_and_Grocery.data,
				mobilePhones_and_Tablets=form.mobilePhones_and_Tablets.data,
				electronics=form.electronics.data,
				sports=form.sports.data,
				home_Furniture_and_Appliances=form.home_Furniture_and_Appliances.data,
				fashion=form.fashion.data,
				health_and_Beauty=form.health_and_Beauty.data,
				toys=form.toys.data
			)

			# Handle product image upload
			product_image = form.product_image.data
			if product_image:
				# Generate a unique filename using UUID
				uuid_filename = str(uuid.uuid1()) + '_' + secure_filename(product_image.filename)
				new_product.image_name = uuid_filename

			# Save the uploaded file to your server
			product_image.save(os.path.join(app.config['IMAGE_FOLDER'], uuid_filename))

			# Add new product to database
			db.session.add(new_product)
			db.session.commit()

			# Redirect to home page or product list page
			return redirect(url_for('views.home'))
		else:
			for field, errors in form.errors.items():
				for error in errors:
					print(f"Error in {field}: {error}", flush=True)

		return render_template('views/create_product.html', form=form)
	else:
		return abort(404)


@views.route('/profile')
@login_required
def profile():
    return render_template('views/profile.html')

@views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfile()
	user = db.get_or_404(User, current_user.id)
	if form.validate_on_submit():
		if bool(form.email.data.strip()):
			user.email = form.email.data
		if bool(form.fname.data.strip()):
			user.first_name = form.fname.data
		if bool(form.lname.data.strip()):
			user.last_name = form.lname.data
		if bool(form.phone.data.strip()):
			user.phone = form.phone.data
		if bool(form.address.data.strip()):
			user.address = form.address.data
		if bool(form.address2.data.strip()):
			user.address2 = form.address2.data
		if bool(form.city.data.strip()):
			user.city = form.city.data
		if bool(form.country.data.strip()):
			user.country = form.country.data
		if bool(form.zipcode.data.strip()):
			user.zip_code = form.zipcode.data
		db.session.commit()
		return redirect(url_for('views.profile'))
	return render_template('views/edit_profile.html', form=form)


@views.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
	product = db.session.execute(db.select(Cart).filter(and_(Cart.user_id == current_user.id, Cart.product_id == product_id))).scalars().first()
	if product is None:
		new_item = Cart(product_id=product_id, user_id=current_user.id)
		db.session.add(new_item)
		db.session.commit()
	return redirect(request.referrer)

@views.route('/cart')
@login_required
def cart():
    items = db.session.execute(db.select(Cart).filter_by(user_id=current_user.id)).scalars()
    product_ids = [item.product_id for item in items]
    cart_products = db.session.execute(db.select(Product).filter(Product.id.in_(product_ids)).order_by(Product.timestamp.desc())).scalars()
    cart_products_list = list(cart_products)
    no_of_items_in_cart = len(cart_products_list)
    total_price = 0
    if cart_products_list:
	    for i in cart_products_list:
	    	total_price += int(i.price)

    return render_template('views/cart.html', products=cart_products_list, total_price=total_price)

@views.route('/delete-cart-item/<int:product_id>')
@login_required
def remove_from_cart(product_id):
	cart_item = db.session.execute(db.select(Cart).filter(and_(Cart.user_id == current_user.id, Cart.product_id == product_id))).scalars().first()
	if cart_item is not None:
		db.session.delete(cart_item)
		db.session.commit()
	return redirect(request.referrer)


@views.route('/add-to-wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_or_remove_from_wishlist(product_id):
	item =  db.session.execute(db.select(WishList).filter(and_(WishList.user_id == current_user.id, WishList.product_id == product_id))).scalars().first()
	if item is not None:
		db.session.delete(item)
		db.session.commit()
	elif item is None:
		new_item = WishList(product_id=product_id, user_id=current_user.id)
		db.session.add(new_item)
		db.session.commit()
	return redirect(request.referrer)

@views.route('/wish-list')
@login_required
def wishlist():
    items = db.session.execute(db.select(WishList).filter_by(user_id=current_user.id)).scalars()
    product_ids = [item.product_id for item in items]
    wishlist_items = list(db.session.execute(db.select(Product).filter(Product.id.in_(product_ids))).scalars())

    return render_template('views/wishlist.html', products=wishlist_items)


@views.route('/checkout')
@login_required
def checkout():
	form = CheckoutForm(phone=current_user.phone, address=current_user.address, address2=current_user.address2, city=current_user.city, country=current_user.country)
	cart_items = list(db.session.execute(db.select(Cart).filter(Cart.user_id == current_user.id)).scalars())
	product_ids = [item.product_id for item in cart_items]
	cart_products = list(db.session.execute(db.select(Product).filter(Product.id.in_(product_ids))).scalars())
	total_price = 0
	if cart_products:
		for i in cart_products:
			total_price += int(i.price)
	if request.method == 'GET' and cart_products:
		return render_template('views/checkout.html', form=form, summary=cart_products, total_price=total_price)
	else:
		return redirect(url_for('views.cart'))


@views.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
	orders = list(db.session.execute(db.select(Orders).filter(Orders.user_id == current_user.id).order_by(Orders.timestamp.desc())).scalars())
	summary = []
	for order in orders:
		order_data_dict = json.loads(order.order_items)
		summary.append({
			'order': order,
			'summary_data': order_data_dict.items()
			})

	return render_template('views/orders.html', orders_summary=summary)

@views.route('/submit_ref_data', methods=['POST'])
def submit_ref_data():
    data = request.json

    global pay_ref
    pay_ref = data['ref']

    return ref

@views.route('/place-order', methods=['POST'])
@login_required
def place_order():
	form = CheckoutForm()
	if form.validate_on_submit():
		global pay_ref
		payment_reference = pay_ref
		
		if not payment_reference:
			flash('Payment was not successful. Please try again.', 'danger')
			return redirect(url_for('views.checkout'))
        
		headers = {
			'Authorization': f"Bearer {app.config['PAYSTACK_SECRET_KEY']}",
			'Content-Type': 'application/json',
		}
		response = requests.get(f'https://api.paystack.co/transaction/verify/{payment_reference}', headers=headers)
		response_data = response.json()

		if not response_data['status'] or response_data['data']['status'] != 'success':
			flash('Payment verification failed. Please try again.', 'danger')
			return redirect(url_for('views.checkout'))

		cart_items = list(db.session.execute(db.select(Cart).filter(Cart.user_id == current_user.id)).scalars())
		product_ids = [item.product_id for item in cart_items]
		cart_products = list(db.session.execute(db.select(Product).filter(Product.id.in_(product_ids))).scalars())

		order = {}
		for item in cart_products:
			order[item.name] = item.price

		total_price = 0
		if cart_products:
			for i in cart_products:
				total_price += int(i.price)

		delivery_details = f'{form.address.data}, {form.city.data}, {form.country.data}'
		if bool(form.address2.data):
			delivery_details = f'{form.address2.data}, {delivery_details}'

		new_order = Orders(user_id=current_user.id, username=f'{current_user.first_name} {current_user.last_name}', order_items=json.dumps(order), delivery_details=delivery_details, total_price=total_price)
		new_order.generate_order_name()

		db.session.add(new_order)

		for item in cart_items:
			db.session.delete(item)

		db.session.commit()
		return redirect(url_for('views.orders'))
	return redirect(url_for('views.checkout'))