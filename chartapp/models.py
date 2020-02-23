from chartapp import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True)
	password = db.Column(db.String(32))
	charts = db.relationship("Chart", backref='user')


class Chart(db.Model):
	__tablename__ = 'chart'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(150))
	author_name = db.Column(db.String(32), db.ForeignKey('user.username'))
	id_by_author = db.Column(db.Integer, nullable=False)
	curr_data = db.relationship("CurrencyData", backref='chart')

	def get_id_by_author(name):
		return Chart.query.filter_by(author_name=name).count()+1


class CurrencyData(db.Model):
	__tablename__ = 'currency_data'
	id = db.Column(db.Integer, primary_key=True)
	chart_id = db.Column(db.Integer, db.ForeignKey('chart.id'))
	uah = db.Column(db.Integer)
	date = db.Column(db.String(10))
