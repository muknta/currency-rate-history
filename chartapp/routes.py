from chartapp import app, db
from flask import render_template, redirect, flash, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
	LoginManager,
	login_user, login_required, logout_user, current_user
)
from .route_handlers import *
from .forms import LoginForm, RegisterForm, ChartCreateForm, ChartUpdateForm
from .models import User, Chart, CurrencyData

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


def db_session_add(new_elem, message=''):
	# good practice of session use from documentation (try-except)
	try:
		db.session.add(new_elem)
		db.session.commit()
		flash(message)
	except:
		db.session.rollback()


@app.route('/')
def index():
	return render_template('index.html', title='CurrChart Index')


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
	form = ChartCreateForm()
    
	if form.validate_on_submit():
		id_by = Chart.get_id_by_author(current_user.username)
		new_chart = Chart(description=form.description.data,
				author_name=current_user.username, id_by_author=id_by)
		message = '{}th chart was created for user "{}"'.format(id_by, current_user.username)
		db_session_add(new_chart, message)

		return redirect(url_for('chart', id_by=id_by))
	return render_template('user.html', name=current_user.username, 
		charts=current_user.charts, form=form, title="User Data")


def get_user_by_username(name):
	return User.query.filter_by(username=name).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('user'))
	form = LoginForm()
    
	if form.validate_on_submit():
		user = get_user_by_username(form.username.data)
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember_me.data)

				flash('Entered as user "{}", remember_me={}'.format(
					form.username.data, form.remember_me.data))
				return redirect(url_for('user'))
		flash('Invalid username or password')
	return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('user'))
	form = RegisterForm()
    
	if form.validate_on_submit():
		if get_user_by_username(form.username.data):
			flash('User "{}" already exist'.format(form.username.data))
			return redirect(url_for('register'))
		else:
			hashed_password = generate_password_hash(form.password.data, method='sha256')
			new_user = User(username=form.username.data, password=hashed_password)
			message = 'Sign Up requested for user "{}".'.format(form.username.data)
			db_session_add(new_user, message)

			return redirect(url_for('login'))
	elif form.submit.data and not form.validate_on_submit():
		flash('Fill the fields. "Username"(max_length=32) and "Password"(max_length=32)')
		return redirect(url_for('register'))
	return render_template('register.html', title='Sign Up', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


def add_to_curr_data(form, chart_id):
	new_curr_data = CurrencyData(uah=form.uah.data, date=form.date.data, chart_id=chart_id)
	query_by_chart_id = CurrencyData.query.filter_by(chart_id=chart_id)
	# count_query == (new_curr_data.id by chart_id)
	count_query = query_by_chart_id.count()+1
	message = 'added: id={}, uah={}, date={}'.format(count_query, form.uah.data, form.date.data)
	db_session_add(new_curr_data, message)


def pop_from_curr_data(form, chart_id):
	query_by_chart_id = CurrencyData.query.filter_by(chart_id=chart_id)
	if query_by_chart_id.first():
		# count_query == (last_elem.id by chart_id)
		count_query = query_by_chart_id.count()
		last_elem = query_by_chart_id.order_by(CurrencyData.id.desc()).first()

		try:
			last_el_by_id = db.session.query(CurrencyData).filter_by(id=last_elem.id).first()
			db.session.delete(last_el_by_id)
			db.session.commit()
			flash('deleted: id={}, uah={}, date={}'.format(
				count_query, last_elem.uah, last_elem.date))
		except:
			db.session.rollback()


def extract_sorted_curr_data(chart_id):
	curr_data = CurrencyData.query.filter_by(chart_id=chart_id).order_by(CurrencyData.date)

	labels, data = [],[]
	for elem in curr_data:
		# each can be in one row but it will be O(2n) instead of O(n)
		labels.append(elem.date)
		data.append(elem.uah)
	return labels, data


@app.route('/chart/<id_by>', methods=['GET', 'POST'])
@login_required
def chart(id_by=0):
	chart_by = next((x for x in current_user.charts if x.id_by_author == int(id_by)), None)
	if not chart_by:
		return jsonify('404: Not Found'), 404
	
	form = ChartUpdateForm()
	if form.add_btn.data and form.validate_on_submit():
		add_to_curr_data(form, chart_by.id)
		return redirect(url_for('chart', id_by=id_by))
	elif form.pop_btn.data:
		pop_from_curr_data(form, chart_by.id)
		return redirect(url_for('chart', id_by=id_by))
	elif form.add_btn.data and not form.validate_on_submit():
		flash("Invalid input. Need to fill 'Date' and 'UAH'(>=0)")
		return redirect(url_for('chart', id_by=id_by))

	labels, data = extract_sorted_curr_data(chart_by.id)
	return render_template('chart.html', chart=chart_by,
		labels=labels, data=data, form=form, title='User Chart')


@app.route('/api-chart', methods=['GET', 'POST'])
def get_api_chart():
    return
