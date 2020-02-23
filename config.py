import os


class Config:
	DEBUG = True
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'thebestcsrfpractice'
	BASE_DIR = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'chart.db')
