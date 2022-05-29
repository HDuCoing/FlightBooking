from flask import render_template, url_for, redirect, request, flash
from sqlalchemy.orm import session, Query

from flaskflights.models import User, Aircraft, AvailableFlights
from flaskflights.forms import LoginForm, RegistrationForm, FlightSelect
from flaskflights import app, db
from sqlalchemy import insert, select


#routes
@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #fixme TypeError: __init__() takes 1 positional argument but 4 were given
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        flash('Thanks for registering with AirDuCoing!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Register")


#todo make search work
@app.route('/book', methods=['GET', 'POST'])
def book():
    form = FlightSelect(request.form)
    flights = AvailableFlights.query
    # If user submits dates - take to listing of available flights in date range
    if request.method == 'POST':
        # specific date
        leave = form.leaveOn.data
        return_on = form.returnOn.data
        location = form.location.data
        
        # day of week - monday is 0 - sunday is 6
        dayLeave = leave.weekday()
        dayReturn = return_on.weekday()
        chosenDateRange = []
        # create a range of weekdays for flight search
        for i in range(dayLeave, dayReturn):
            chosenDateRange.append(i)

        if location == 'Dairy Flat':
            sess = session()
            query = Query([AvailableFlights], session=sess)
            print(query.column_descriptions)
            # friday morning - to rotorua then sydney - syberjet

            # monday through friday; - cirrus jets
            # morning - to rotorua
            # late afternoon - to rotorua

            # tuesday and friday - to tuuta - hondajets
            # monday - to tekapo - hondajets
            # monday wednesday friday - morning - to great barrier island - cirrus jets
        elif location == 'Rotorua':
            # friday morning - to sydney - syberjet

            # monday through friday; - cirrus jets
            # noon - to dairy flat
            # evening - to dairy flat
            None
        elif location == 'Tuuta':
            # wednesday and saturday - to dairy flat - HondaJets
            None
        elif location == 'Sydney':
            # sunday afternoon - to dairy flat - syberjet
            None
        elif location == 'Tekapo':
            # friday - to dairy flat - hondajet
            None
        elif location == 'Great Barrier Island':
            # monday, friday, saturday - to dairy flat - cirrus jets
            None
        return render_template('flight_info.html', query=query)
    return render_template('book.html', form=form, title="Book", flights=flights)
