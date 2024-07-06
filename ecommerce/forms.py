from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import email_validator
from .models import User
from . import db

class SignUP(FlaskForm):
	email = StringField("Email Address", validators=[DataRequired('Please provide an email'), Email(message='Please enter a valid email')])
	password1 = PasswordField("Password" , validators=[DataRequired('Please enter your password'), Length(min=8, max=20, message="Password must be 8-20 characters long")])
	password2 = PasswordField("Confirm Password" , validators=[DataRequired('Please confirm your password'), EqualTo('password1', "Passwords do not match")])
	submit = SubmitField('Submit')

	def validate_email(self, email):
		if email.errors:
			return
		user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
		if user is not None:
			raise ValidationError("Email address already in use")

class Login(FlaskForm):
	email = StringField("Email Address", validators=[DataRequired('Please provide an email'), Email(message='Please enter a valid email')])
	password = PasswordField("Password" , validators=[DataRequired('Please enter your password'), Length(min=8, max=20, message="Password must be 8-20 characters long")])
	submit = SubmitField('Submit')

	def validate_email(self, email):
		if email.errors:
			return
		user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
		if user is None:
			raise ValidationError("User does not exist")


class NewProduct(FlaskForm):
	name = StringField('Product Name', validators=[DataRequired()])
	seller = StringField('Seller', validators=[DataRequired()])
	price = IntegerField('Price', validators=[DataRequired()])
	food_and_Grocery = BooleanField('Food & Grocery', false_values=(False, 'false'))
	mobilePhones_and_Tablets = BooleanField('Mobile Phones & Tablets', false_values=(False, 'false'))
	electronics = BooleanField('Electronics', false_values=(False, 'false'))
	sports = BooleanField('Sports', false_values=(False, 'false'))
	home_Furniture_and_Appliances = BooleanField('Home, Furniture & Appliances', false_values=(False, 'false'))
	fashion = BooleanField('Fashion', false_values=(False, 'false'))
	health_and_Beauty = BooleanField('Health & Beauty', false_values=(False, 'false'))
	toys = BooleanField('Toys', false_values=(False, 'false'))
	submit = SubmitField('Submit')
