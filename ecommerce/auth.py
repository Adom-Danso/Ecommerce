from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, Product
from .forms import SignUP, Login
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	form = SignUP()
	if current_user.is_authenticated:
		return redirect(url_for('views.home'))
	if form.validate_on_submit():
		new_user = User(email=form.email.data)
		new_user.set_password(form.password1.data)
		new_user.set_username()
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user, remember=True)
		flash("Your account has been created")
		return redirect(url_for('views.home'))
	return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = Login()
	print(form.email.data, flush=True)
	print(form.password.data, flush=True)
	if current_user.is_authenticated:
		print('current_user.is_authenticated', flush=True)
		return redirect(url_for('views.home'))
	print(form.validate_on_submit(), flush=True)
	if form.validate_on_submit():
		print('form has been validated', flush=True)
		user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()
		print('a query has been made', flush=True)
		if user.verify_password(form.password.data):
			print('password has been verified', flush=True)
			login_user(user, remember=True)
			flash('Successfully logged into your account')
			return redirect(url_for('views.home'))
		else:
			print('password has not been verified', flush=True)
			flash('Incorrect email or password')
	print('form did not even validate', flush=True)
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(request.referrer)
