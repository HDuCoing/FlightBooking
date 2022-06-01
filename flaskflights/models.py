from sqlalchemy import ForeignKey, Column, Integer, MetaData
from sqlalchemy.orm import relationship
from flaskflights import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user details
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    password = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
# flight booking info for user's account info page
class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    bookingRef = db.Column(db.String(100), nullable=False)
    flightDates = db.Column(db.Integer, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    payment = db.Column(db.Integer, nullable=False)
    #bookedFlight = relationship('AvailableFlights')

    def __repr__(self):
        return f"Booking('{self.bookingRef}', '{self.flightDates}')"

# aircraft name + model, and capacity
class Aircraft(db.Model):
    __tablename__ = 'aircraft'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    model = db.Column(db.String(30), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    flightChild = relationship("AvailableFlights")

    def __repr__(self):
        return f"Aircraft('{self.name}, {self.model}','{self.capacity}')"

class AvailableFlights(db.Model):
    __tablename__ = 'available_flights'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeOfFlight = db.Column(db.Integer, nullable=False)
    dateOfFlight = db.Column(db.Date, nullable=False)
    dayOfFlight = db.Column(db.String, nullable=False)
    flyingFrom = db.Column(db.String, nullable=False)
    stopsAt = db.Column(db.String, nullable=True)
    flyingTo = db.Column(db.String, nullable=False)
    aircraft = Column(Integer, ForeignKey("aircraft.id"))
    seatsLeft = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Aircraft('{self.timeOfFlight}','{self.dateOfFlight}','{self.dayOfFlight}','{self.flyingFrom}','{self.stopsAt}','{self.flyingTo}','{self.aircraft}', '{self.seatsLeft}')"
