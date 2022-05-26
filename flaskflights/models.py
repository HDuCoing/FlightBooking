from sqlalchemy import func
from sqlalchemy.orm import session
from flaskflights.forms import FlightSelect, RegistrationForm, LoginForm

from flaskflights import db

aircrafts = ['SyberJet SJ30i',
             'Cirrus SF50 1',
             'Cirrus SF50 2',
             'HondaJet Elite 1',
             'HondaJet Elite 2']

# user details
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

# flight booking dates to be returned when you search for a flight
class BookingDates(db.Model):
    __tablename__ = 'bookingdates'
    id = db.Column(db.Integer, primary_key=True)
    leaveOn = db.Column(db.Integer, nullable=False)
    returnOn = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"('{self.leaveOn}','{self.returnOn}')"

# flight booking info for user's account info page
class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    bookingRef = db.Column(db.String(100), nullable=False)
    flightDates = db.Column(db.Integer, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)

    def __repr__(self):
        return f"Booking('{self.bookingRef}', '{self.flightDates}')"

# aircraft name + model, and capacity
class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Aircraft('{self.model}','{self.capacity}')"

class AvailableFlights(db.Model):
    __tablename__ = 'available_flights'
    id = db.Column(db.Integer, primary_key=True)
    # date equals flight select form output
    dayOfFlight = db.Column(db.String, nullable=False)
    aircrafts = db.Column(db.String, nullable=False)
    seatsAvailable = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"AvailableFlights('{self.date}', '{self.time}')"

