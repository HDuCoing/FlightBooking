from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flaskflights import db

# user details
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

# flight booking info
class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    bookingRef = db.Column(db.String(100), nullable=False)
    flightDates = db.Column(db.Integer, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)

    def __repr__(self):
        return f"Booking('{self.bookingRef}', '{self.flightDates}')"

aircrafts = ['SyberJet SJ30i',
             'Cirrus SF50 1',
             'Cirrus SF50 2',
             'HondaJet Elite 1',
             'HondaJet Elite 2']

class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Aircraft('{self.model}','{self.capacity}')"

class AvailableFlights(db.Model):
    __tablename__ = 'available_flights'
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    aircrafts = db.Column(db.String, nullable=False)
    seatsAvailable = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"AvailableFlights('{self.date}', '{self.time}')"

# will be aircraft + hour departure + seat number
generateReference = []

#forms--------------
class FlightSelect(FlaskForm):
    leaveOn = DateField('Leave On', format='%Y-%m-%d')
    returnOn = DateField('Return On', format='%Y-%m-%d')
    submit = SubmitField('Submit')


# account registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# account login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')