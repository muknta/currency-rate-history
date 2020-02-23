from flask_wtf import FlaskForm
from wtforms import (
	StringField,
	IntegerField,
	PasswordField,
	BooleanField,
	SubmitField
)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class ChartCreateForm(FlaskForm):
	description = StringField('Description:', render_kw={"placeholder": "Description"})
	submit = SubmitField('Create Chart')


class ChartUpdateForm(FlaskForm):
	uah = IntegerField('UAH to USD', validators=[DataRequired()])
	date = DateField('Date', validators=[DataRequired()])
	add_btn = SubmitField('Add')
	pop_btn = SubmitField('Pop')
