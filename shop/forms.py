from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from shop.models import User


class RegistrationForm(FlaskForm):
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=1,max=20)])
	last_name = StringField('Surname', validators=[DataRequired(), Length(min=1, max=20)])
	address = StringField('Address', validators=[DataRequired(), Length(min=1, max=50)])
	username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), Regexp('^.{8,}$', message='Your password must be more than 8 characters long.')])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
	submit = SubmitField('Register')
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exist. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CheckoutForm(FlaskForm):
	card_name  = StringField('Name on Card', validators=[DataRequired()])
	card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16, message='Invalid details.')])
	expiry_date = StringField('Expiry Date(mm/yyyy)', validators=[DataRequired(), Length(min=7, max=7, message='Invalid details')])
	cvc = StringField('CVC', validators=[DataRequired(), Length(min=3, max=4, message='Invalid details')])
	submit = SubmitField('Confirm Payment')