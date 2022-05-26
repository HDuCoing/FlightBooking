from models import LoginForm, RegistrationForm, FlightSelect, AvailableFlights, Aircraft, Booking, User


# get flights available based on dates
def flightsAvailable():
    for column in AvailableFlights.c:
        print(column)