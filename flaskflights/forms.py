from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# flight select from date field inputs on /book
class FlightSelect(FlaskForm):
    locations=["Dairy Flat", "Rotorua", "Sydney", "Tuuta", "Great Barrier Island", "Tekapo"]
    location = SelectField('Fly From', choices=locations, validators=[DataRequired()])
    leaveOn = DateField('Leave On', format='%Y-%m-%d')
    returnOn = DateField('Return On', format='%Y-%m-%d')
    submit = SubmitField('Submit')


# account registration - /register
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# account login - /login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

