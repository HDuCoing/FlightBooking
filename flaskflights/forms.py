from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flaskflights.models import User

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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken.')

    def validate_email(self, email):
        email = User.query.filter_by(username=email.data).first()
        if email:
            raise ValidationError('Email is taken.')


# account login - /login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

