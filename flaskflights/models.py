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
# flight booking info for user's account info page
class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    # user ID
    user = db.Column(db.Integer, nullable=False)
    bookingRef = db.Column(db.String(100), nullable=False)
    flightDates = db.Column(db.Integer, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    aircraft = db.Column(db.String)

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

