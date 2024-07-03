from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
	app = Flask(__name__)
	app.config.from_object('config.DevelopmentConfig')

	db.init_app(app)
	login_manager.init_app(app)
	login_manager.login_view = "auth.login"
	login_manager.login_message = "Bonvolu ensaluti por uzi tiun paĝon."

	from .views import views
	from .auth import auth
	from .admin import admin

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/auth')
	app.register_blueprint(admin, url_prefix='/admin')

	from .models import Product, User, Cart

	with app.app_context():
	    db.create_all()

	@login_manager.user_loader
	def load_user(user_id):
	    return User.query.get(user_id)
	return app