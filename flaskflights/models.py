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

class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    flights = db.relationship('Flight', backref='aircraft', lazy=True, uselist=True)

# --------------- for flight select -------------------
flights = ['8:00 A.M.', '10:00 A.M.', '1:00 P.M.', '4:00 P.M.']
aircrafts = ['SyberJet SJ30i', 'Cirrus SF50 1', 'Cirrus SF50 2', 'HondaJet Elite 1', 'HondaJet Elite 2']
# will be aircraft + hour departure + seat number
generateReference = []

#forms--------------
class FlightSelect(FlaskForm):
    leaveOn = DateField('Leave On', format='%Y-%m-%d' )
    returnOn = DateField('Return On', format='%Y-%m-%d')
    timeLeave = RadioField('Time of Flight', choices=[flights], validators=[DataRequired()])
    timeReturn = RadioField('Time of Flight', choices=[flights], validators=[DataRequired()])

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