from . import admin_panel, db
from .models import User, Product
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
	column_exclude_list = ['password', 'timestamp']
	form_excluded_columns = ['password', 'email', 'username', 'timestamp', 'first_name', 'last_name', 'country', 'address', 'address2','city', 'zip_code', 'phone']
	form_choices = {'role': [('normal', 'normal'), ('admin', 'admin')]}


	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == 'admin'

	def inaccessible_callback(self, name, **kwargs):
		return abort(403)


class ProductView(ModelView):
	page_size = 50
	can_view_details = True
	column_searchable_list = ['name']
	column_exclude_list = ['timestamp']
	form_excluded_columns = ['timestamp']

	def is_accessible(self):
		return current_user.is_authenticated and current_user.role == 'admin'

	def inaccessible_callback(self, name, **kwargs):
		return abort(403)


admin_panel.add_view(UserView(User, db.session))
admin_panel.add_view(ProductView(Product, db.session))
