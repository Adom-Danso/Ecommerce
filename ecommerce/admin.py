from . import admin_panel, db
from .models import User, Product, Orders
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, abort

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == 'admin'

	def inaccessible_callback(self, name, **kwargs):
		return abort(403)

class UserView(ModelView):
	can_delete = False
	can_create = False
	column_editable_list = ['role']
	column_searchable_list = ['id', 'first_name', 'last_name', 'country', 'city', 'email']
	column_exclude_list = ['password', 'timestamp']
	form_excluded_columns = ['password', 'email', 'timestamp', 'first_name', 'last_name', 'country', 'address', 'address2','city', 'zip_code', 'phone']
	form_choices = {'role': [('normal', 'normal'), ('admin', 'admin')]}


	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == 'admin'

	def inaccessible_callback(self, name, **kwargs):
		return abort(403)


class ProductView(ModelView):
	page_size = 50
	can_view_details = True
	column_searchable_list = ['name', 'id']
	column_exclude_list = ['timestamp']
	form_excluded_columns = ['timestamp']

	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == 'admin'

	def inaccessible_callback(self, name, **kwargs):
		return abort(403)

class OrderView(ModelView):
	page_size = 50
	can_delete = False
	can_create = False
	can_view_details = True
	column_searchable_list = ['status', 'user_id', 'order_items']
	column_exclude_list = ['timestamp']
	form_excluded_columns = ['timestamp', 'user_id', 'order_items']
	column_editable_list = ['status']
	form_choices = {'status': [('pending', 'pending'), ('processing', 'processing'), ('shipped', 'shipped'), ('dilivered', 'dilivered'), ('canceled', 'canceled')]}

	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == 'admin'

	def inaccessible_callback(self, name, **kwargs):
		return abort(403)

admin_panel.add_view(UserView(User, db.session))
admin_panel.add_view(ProductView(Product, db.session))
admin_panel.add_view(OrderView(Orders, db.session))
