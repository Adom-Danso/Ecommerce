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
		return redirect(url_for('views.home'))  # redirect user to home page if already logged in

	if form.validate_on_submit():
		new_user = User(email=str(form.email.data).strip(), first_name=str(form.fname.data).strip(), last_name=str(form.lname.data).strip())
		new_user.set_password(form.password1.data)
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user, remember=True)
		flash("Your account has been created")
		return redirect(url_for('views.home'))
	return render_template('auth/signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = Login()
	if current_user.is_authenticated: 
		return redirect(url_for('views.home')) # redirect user to home page if already logged in

	if form.validate_on_submit():
		
		user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar()

		if user.verify_password(form.password.data):
			login_user(user, remember=True)
			flash('Successfully logged into your account')
			return redirect(url_for('views.home'))
		else:
			flash('Incorrect email or password')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(request.referrer)
