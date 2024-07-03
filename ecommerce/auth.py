from flask import Blueprint, render_template, redirect, url_for
from .models import User
from .forms import SignUP
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	form = SignUP()
	if form.validate_on_submit():
		new_user = User(email=form.email.data)
		new_user.set_password(form.password1.data)
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('views.home'))
	return render_template('auth/signup.html', form=form)