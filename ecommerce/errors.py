from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404) # catching page not found error(404 errors)
def not_found_error(error):
	return render_template('error/404.html'), 404

@errors.app_errorhandler(403) # catching forbiden error(403 errors)
def forbiden_error(error):
	return render_template('error/403.html'), 403