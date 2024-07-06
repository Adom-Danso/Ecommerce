import secrets


class Config(object):
	DEBUG = False
	TESTING = False
	SESSION_COOKIE_SECURE = True
	SECRET_KEY = secrets.token_hex(20)


class DevelopmentConfig(Config):
	DEBUG = True
	SESSION_PROTECTION = "strong"
	SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
	FLASK_ADMIN_SWATCH = 'slate'
	