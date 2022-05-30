from flask import render_template, url_for, redirect, request, flash
from sqlalchemy import select, engine, MetaData
from sqlalchemy.orm import session, Mapper

from flaskflights.models import User, Aircraft, AvailableFlights
from flaskflights.forms import LoginForm, RegistrationForm, FlightSelect
from flaskflights import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


#routes
@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed. Please check username and password.', 'error')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Thanks for registering with AirDuCoing!, {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Register")


#todo make search work
@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = FlightSelect(request.form)
    # If user submits dates - take to listing of available flights in date range
    if request.method == 'POST':
        headings = ('Flying From', 'Stops', 'Flying To', 'Date', 'Time', 'Day Of Flight', 'Aircraft', 'Seats Left')
        # specific date
        leave = form.leaveOn.data
        return_on = form.returnOn.data
        location = form.location.data
        
        # day of week - monday is 0 - sunday is 6
        dayLeave = leave.weekday()
        dayReturn = return_on.weekday()
        chosenDateRange = []
        # create a range of weekdays for flight search

        #todo if from sydney, diff time zone
        for i in range(dayLeave, dayReturn):
            chosenDateRange.append(i)
        flightFrom = db.session.query(AvailableFlights.flyingFrom)\
            .filter(AvailableFlights.flyingFrom==location)
        stopsAt = db.session.query(AvailableFlights.stopsAt)\
            .filter(AvailableFlights.flyingFrom==location)
        flightTo = db.session.query(AvailableFlights.flyingTo)\
            .filter(AvailableFlights.flyingFrom==location)
        date = db.session.query(AvailableFlights.dateOfFlight)\
            .filter(AvailableFlights.flyingFrom==location)
        time = db.session.query(AvailableFlights.timeOfFlight)\
            .filter(AvailableFlights.flyingFrom==location)
        dayOf = db.session.query(AvailableFlights.dayOfFlight)\
            .filter(AvailableFlights.flyingFrom==location)
        aircraft = db.session.query(AvailableFlights.aircraft)\
            .filter(AvailableFlights.flyingFrom==location)
        seats = db.session.query(AvailableFlights.seatsLeft)\
            .filter(AvailableFlights.flyingFrom==location)


        return render_template('flight_info.html',
                               headings=headings,
                               flyingFrom=flightFrom,
                               stopsAt=stopsAt,
                               flightTo=flightTo,
                               date=date,
                               time=time,
                               dayOf=dayOf,
                               aircraft=aircraft,
                               seats=seats
                               )
    return render_template('book.html', form=form, title="Book")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route('/confirmbooking')
@login_required
def confirm_booking():

    return render_template('confirm_booking.html', title="Confirm")