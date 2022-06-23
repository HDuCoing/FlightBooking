from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from flaskflights import app, db, bcrypt
from flaskflights.forms import LoginForm, RegistrationForm, FlightSelect
from flaskflights.models import User, AvailableFlights, Booking, FlightClub

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    return render_template('home.html', title='Home')

# Point club system, if user is logged in and theyre not already a member they may join
@app.route("/flightclub", methods=['GET', 'POST'])
def flightclub():
    if request.method=="POST":
        # If user isn't logged in, redirect
        if current_user.is_anonymous:
            return redirect(url_for('login'))
        else:
            # If user is already in system, redirect
            for members in FlightClub.query.filter(FlightClub.member==current_user.username):
                    if members:
                        flash("Already a member", 'error')
                        return redirect(url_for('account'))
            member = FlightClub(member=current_user.username, points=0)
            db.session.add(member)
            db.session.commit()
    return render_template('flightclub.html', title='Join | Flight Club')

# Simple login system that validates user information
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
        flights = AvailableFlights.query.filter(AvailableFlights.flyingFrom==location,AvailableFlights.dateOfFlight==leave)
        return render_template('flight_info.html',headings=headings,flights=flights)
    return render_template('book.html', form=form, title="Book")

@app.route('/confirm')
@login_required
def confirm(flight):
    map_img = ""
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
        if flights.seatsLeft <= 0:
            flash("Flight is full.", 'error')
        elif flights:
            flightList = [flights]
            flight = flightList[0]
            # Generate a booking reference based on some flight information
            bookingRef = ("REF",str(flight.id),str(flight.seatsLeft))
            bookingRef = ''.join(bookingRef)
            titles=['Time: ', 'Date: ', 'From: ', 'Stops: ', 'To: ', 'Aircraft', 'Price: ']
            booking = Booking(bookingRef=bookingRef,
                              price=price,
                              user=current_user.username,
                              seat=flight.seatsLeft,
                              flight=flight.id)
            db.session.add(booking)
            for member in FlightClub.query.filter(FlightClub.member==current_user.username):
                if member:
                    if flyTo == 'Sydney':
                        member.points = member.points+1
                    else:
                        member.points = member.points+0.5
            flash("Booking Complete!", "success")
            flight.seatsLeft = flight.seatsLeft-1
        else:
            flash("No seats left on this flight", 'error')
        # define image to show map of flight path on confirmation
        if flight.flyingFrom == "Dairy Flat":
            if flight.flyingTo == "Rotorua":
                map_img = "DFtoROTO.png"
            if flight.flyingTo == "Great Barrier Island":
                map_img = "DFtoGBI.png"
            if flight.flyingTo == "Tekapo":
                map_img = "DFtoTEKAPO.png"
            if flight.flyingTo == "Sydney":
                map_img = "DFtoROTOtoSYD.png"
            if flight.flyingTo == "Tuuta":
                map_img = "DFtoTUUTA.png"
        if flight.flyingFrom == "Rotorua":
            if flight.flyingTo == "Dairy Flat":
                map_img = "ROTOtoDF.png"
            if flight.flyingTo == "Sydney":
                map_img = "ROTOtoSYD.png"
        if flight.flyingFrom == "Sydney":
            if flight.flyingTo == "Dairy Flat":
                map_img = "SYDtoDF.png"
    db.session.commit()
    return render_template('confirm_booking.html', title="Confirm", flight=flight_info, reference=bookingRef, titles=titles, map=map_img)

@app.route("/explore")
def explore():
    headings = ('Flying From', 'Stops', 'Flying To', 'Date', 'Day Of Flight', 'Time', 'Aircraft', 'Seats Left')
    flights = AvailableFlights.query.all()
    return render_template('explore_flights.html', title='Explore', headings=headings, flights=flights)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    points=None
    for member in FlightClub.query.filter(FlightClub.member==current_user.username):
        if member:
            points = member.points
    if request.method=="GET":
        args = request.args
        for element in args:
            flightRef = element
            if flightRef:
                for b in Booking.query.filter(Booking.user == current_user.username, Booking.bookingRef == flightRef):
                    for f in AvailableFlights.query.filter(AvailableFlights.id == b.flight):
                        f.seatsLeft = f.seatsLeft+1
                        for member in FlightClub.query.filter(FlightClub.member == current_user.username):
                            if member:
                                if f.flyingTo == 'Sydney':
                                    member.points = member.points - 1
                                else:
                                    member.points = member.points - 0.5
                        db.session.delete(b)
                        db.session.commit()

    headings = ('Booking Reference', 'Flying From', 'Stops', 'Flying To', 'Date', 'Time', 'Aircraft', 'Seat','Price', 'Cancel')
    flightList = []
    bookingRefs = []
    book = None
    for book in Booking.query.filter(Booking.user == current_user.username):
        for flight in AvailableFlights.query.filter(AvailableFlights.id==book.flight):
            aBooking = book
            aFlight = flight
            flightList.append(aFlight)
            bookingRefs.append(aBooking.bookingRef)
    return render_template('account.html', title='Account', headings=headings, list=flightList, refs=bookingRefs, booking=book, points=points)

