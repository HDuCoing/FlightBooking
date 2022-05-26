from forms import LoginForm, RegistrationForm, FlightSelect
from models import  AvailableFlights, Aircraft, Booking, User


# get flights available based on dates
def flightsAvailable():
    for flight in AvailableFlights.c:
        return flight

# get user info - for authenticating
def userAuth():
    for user in User.c:
        return [user.id, user.username, user.password]

