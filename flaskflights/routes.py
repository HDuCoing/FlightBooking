from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.orm import session
from sqlalchemy import update
from flaskflights import app, db, bcrypt
from flaskflights.forms import LoginForm, RegistrationForm, FlightSelect
from flaskflights.models import User, AvailableFlights, Booking


#routes
@app.route("/")
@app.route("/home")
@app.route("/index")
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
    #todo
    if request.method == 'GET':
        args = request.args
        for element in args:
            flight = element
            if flight:
                return confirm(flight)

    if request.method == 'POST':
        headings = ('Flying From', 'Stops', 'Flying To', 'Date', 'Day Of Flight', 'Time', 'Aircraft', 'Seats Left', 'Select')
        # specific date
        leave = form.leaveOn.data
        location = form.location.data
        # create a range of weekdays for flight searc
        #todo if from sydney, diff time zone
        flights = AvailableFlights.query.filter(AvailableFlights.flyingFrom==location,AvailableFlights.dateOfFlight==leave)
        return render_template('flight_info.html',headings=headings,flights=flights)
    return render_template('book.html', form=form, title="Book")

@app.route('/confirm')
def confirm(flight):
    # isolate flight info for client's view.
    flightContent = flight.strip("Aircraft")
    flightContent = flightContent.strip("(")
    flightContent = flightContent.strip(")")
    flightContent = flightContent.split(",")
    time = "Time: " + flightContent[0]
    date = "Date: " + flightContent[1]
    flyFrom = "Flying From: " + flightContent[3]
    stopAt = "Stops At: " + flightContent[4]
    flyTo = "Flying To: " + flightContent[5]
    aircraft = "Aircraft: " + flightContent[6]
    price = "Price: $50"
    if "Sydney" in flyTo:
        price = "Price: $200"
    flight_info = [time, date, flyFrom, stopAt, flyTo, aircraft, price]
    #todo add flight to user's profile
    booking = Booking(current_user, price, flight)
    db.session.add(booking)
    # update flight capacity
    update(AvailableFlights)\
        .where(AvailableFlights.c.id == flight.c.id)\
        .values(capacity=flight.capacity-1)
    db.session.commit()
    flash("Booking Complete!", "success")
    return render_template('confirm_booking.html', title="Confirm", flight=flight_info)

@app.route("/explore")
def explore():
    headings = ('Flying From', 'Stops', 'Flying To', 'Date', 'Day Of Flight', 'Time', 'Aircraft', 'Seats Left')
    flights = AvailableFlights.query.all()
    return render_template('explore_flights.html', title='Explore', headings=headings, flights=flights)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

