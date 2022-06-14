from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from flaskflights import app, db, bcrypt
from flaskflights.forms import LoginForm, RegistrationForm, FlightSelect
from flaskflights.models import User, AvailableFlights, Booking, Aircraft


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


@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = FlightSelect(request.form)
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
    time = flightContent[0].strip("'")
    date = flightContent[1].strip("'")
    flyFrom = flightContent[3].strip("'")
    stopAt = flightContent[4].strip("'")
    flyTo = flightContent[5].strip("'")
    aircraft = flightContent[6].strip("'")
    # set the price based on destination
    price = 50
    if "Sydney" in flyTo:
        price = 200
    flight_info = [time, date, flyFrom, stopAt, flyTo, aircraft, price]
    # Search through flights and update seats/ add booking
    for flights in AvailableFlights.query.filter(AvailableFlights.timeOfFlight==time, AvailableFlights.dateOfFlight==date, AvailableFlights.flyingFrom==flyFrom, AvailableFlights.flyingTo==flyTo):
        if flights:
            flightList = [flights]
            flight = flightList[0]
            bookingRef = (flyTo,str(flight.seatsLeft))
            bookingRef = "".join(bookingRef)
            titles=['Time: ', 'Date: ', 'From: ', 'Stops: ', 'To: ', 'Aircraft', 'Price: ']
            booking = Booking(bookingRef=bookingRef,
                              price=price,
                              user=current_user.username,
                              seat=flight.seatsLeft,
                              flight=flight.id)
            flash("Booking Complete!", "success")
            flight.seatsLeft = flight.seatsLeft-1
    db.session.add(booking)
    db.session.commit()
    return render_template('confirm_booking.html', title="Confirm", flight=flight_info, reference=bookingRef, titles=titles)

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
    headings = ('Booking Reference', 'Flying From', 'Stops', 'Flying To', 'Date', 'Time', 'Aircraft', 'Seat','Price', 'Cancel')
    for book in Booking.query.filter(Booking.user==current_user.username):
        for flight in AvailableFlights.query.filter(AvailableFlights.id==book.id):
            aBooking = book
            aFlight = flight
    return render_template('account.html', title='Account', headings=headings, booking=aBooking, flight=aFlight)

