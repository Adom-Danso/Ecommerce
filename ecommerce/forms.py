from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, SelectField, TelField, SearchField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from flask_wtf.file import FileField, FileRequired
import email_validator
from .models import User
from . import db


#===============signup form============
class SignUP(FlaskForm):
	fname = StringField('First name', validators=[DataRequired('Please enter your first name')])
	lname = StringField('Last name', validators=[DataRequired('Please enter your last name')])
	email = StringField("Email Address", validators=[DataRequired('Please enter an email'), Email(message='Please enter a valid email')])
	password1 = PasswordField("Password" , validators=[DataRequired('Please enter your password'), Length(min=8, max=20, message="Password must be 8-20 characters long")])
	password2 = PasswordField("Confirm Password" , validators=[DataRequired('Please confirm your password'), EqualTo('password1', "Passwords do not match")])
	submit = SubmitField('Submit')

	#============checking whether email already exists in the database==============
	def validate_email(self, email):
		if email.errors:
			return #============return nothing if an error alreay occured=====
		user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
		if user is not None:
			raise ValidationError("Email address already in use")


#===================Login form==============
class Login(FlaskForm):
	email = StringField("Email Address", validators=[DataRequired('Please enter an email'), Email(message='Please enter a valid email')])
	password = PasswordField("Password" , validators=[DataRequired('Please enter your password'), Length(min=8, max=20, message="Password must be 8-20 characters long")])
	submit = SubmitField('Submit')

	#============checking whether email already exists in the database==============
	def validate_email(self, email):
		if email.errors:
			return #============return nothing if an error alreay occured=====
		user = db.session.execute(db.select(User).filter_by(email=email.data)).scalar()
		if user is None:
			raise ValidationError("User does not exist")

#===================Form for adding new products=========
class NewProduct(FlaskForm):
	product_image = FileField("Product image", validators=[FileRequired('Product image is required')])
	name = StringField('Product Name', validators=[DataRequired('Please enter product name')])
	description = TextAreaField('Product description', validators=[DataRequired('please enter product description')])
	price = DecimalField('Price', places=2, validators=[DataRequired('Please enter product price')])
	food_and_Grocery = BooleanField('Food & Grocery', false_values=(False, 'false'))
	mobilePhones_and_Tablets = BooleanField('Mobile Phones & Tablets', false_values=(False, 'false'))
	electronics = BooleanField('Electronics', false_values=(False, 'false'))
	sports = BooleanField('Sports', false_values=(False, 'false'))
	home_Furniture_and_Appliances = BooleanField('Home, Furniture & Appliances', false_values=(False, 'false'))
	fashion = BooleanField('Fashion', false_values=(False, 'false'))
	health_and_Beauty = BooleanField('Health & Beauty', false_values=(False, 'false'))
	toys = BooleanField('Toys', false_values=(False, 'false'))
	submit = SubmitField('Submit')


class EditProfile(FlaskForm):
	fname = StringField('First name', validators=[DataRequired()])
	lname = StringField('Last name', validators=[DataRequired()])
	phone = TelField('Phone', validators=[DataRequired()])
	email = StringField("Email Address", validators=[DataRequired(), Email(message='Please enter a valid email')])
	address = StringField('Address', validators=[Optional()])
	address2 = StringField('Address 2', validators=[Optional()])
	city = StringField('City', validators=[Optional()])
	country = SelectField('Country', choices=[('Ghana'), ('Nigeria'), ('Togo')], validators=[Optional()])
	zipcode = StringField('Zip code', validators=[Optional()])

class CheckoutForm(FlaskForm):
	phone = TelField('Phone', validators=[DataRequired()])
	address = StringField('Address', validators=[DataRequired()])
	address2 = StringField('Address 2', validators=[Optional()])
	city = StringField('City', validators=[DataRequired()])
	country = SelectField('Country', choices=[('Ghana'), ('Nigeria'), ('Togo')], validators=[DataRequired()])

class SearchForm(FlaskForm):
	search = StringField('Search...')
	submit = SubmitField('Search')