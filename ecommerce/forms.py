from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import email_validator

class SignUP(FlaskForm):
	email = StringField("Email Address", validators=[DataRequired(), Email()])
	password1 = PasswordField("Password" , validators=[DataRequired(), Length(min=8, max=20)])
	password2 = PasswordField("Confirm Password" , validators=[DataRequired(), EqualTo('password1', "Passwords do not match")])
	submit = SubmitField('Submit')	

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
