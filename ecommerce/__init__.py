from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()
admin_panel = Admin()

def create_app():
	app = Flask(__name__)

	load_dotenv()
	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	app.config['PAYSTACK_PUBLIC_KEY'] = os.getenv('PAYSTACK_PUBLIC_KEY')
	app.config['PAYSTACK_SECRET_KEY'] = os.getenv('PAYSTACK_SECRET_KEY')
	app.config['IMAGE_FOLDER'] = 'ecommerce/static/images'
	app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
	app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  

	app.config['SESSION_COOKIE_SECURE'] = True
	app.config['SESSION_PROTECTION'] = "strong"
	app.config['FLASK_ADMIN_SWATCH'] = 'slate'



	from .admin import MyAdminIndexView

	db.init_app(app)
	login_manager.init_app(app)
	login_manager.login_view = "auth.login"
	login_manager.login_message = "Please login in to continue"
	login_manager.session_protection = "strong"
	admin_panel.init_app(app, index_view=MyAdminIndexView())

	from .views import views
	from .auth import auth
	from .errors import errors

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(errors, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/auth')

	from .models import Product, User, Cart, WishList, Orders

	with app.app_context():
	    db.create_all()

	@login_manager.user_loader
	def load_user(user_id):
	    return User.query.get(user_id)
	    
	return app