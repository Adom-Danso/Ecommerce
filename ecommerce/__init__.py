from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin


db = SQLAlchemy()
login_manager = LoginManager()
admin_panel = Admin()

def create_app():
	app = Flask(__name__)
	app.config.from_object('config.DevelopmentConfig')

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

	from .models import Product, User, Cart, WishList

	with app.app_context():
	    db.create_all()

	@login_manager.user_loader
	def load_user(user_id):
	    return User.query.get(user_id)
	    
	return app