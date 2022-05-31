from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required

from flaskflights import app, db, bcrypt
from flaskflights.forms import LoginForm, RegistrationForm, FlightSelect
from flaskflights.models import User, AvailableFlights

import pandas as pd

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
    # If user submits dates - take to listing of available flights in date range
    if request.method == 'POST':
        headings = ('Select', 'Flying From', 'Stops', 'Flying To', 'Date', 'Day Of Flight', 'Time', 'Aircraft', 'Seats Left')
        # specific date
        leave = form.leaveOn.data
        location = form.location.data
        # day of week - monday is 0 - sunday is 6
        dayLeave = leave.weekday()
        # create a range of weekdays for flight search
        #todo if from sydney, diff time zone
        flights = AvailableFlights.query.filter(AvailableFlights.flyingFrom==location,AvailableFlights.dateOfFlight==leave)
        if dayLeave == 0:
            dayLeave = "Monday"
        if dayLeave == 1:
            dayLeave = "Tuesday"
        if dayLeave == 2:
            dayLeave = "Wednesday"
        if dayLeave == 3:
            dayLeave = "Thursday"
        if dayLeave == 4:
            dayLeave = "Friday"
        if dayLeave == 5:
            dayLeave = "Saturday"
        if dayLeave == 6:
            dayLeave = "Sunday"
        return render_template('flight_info.html',
                               headings=headings,
                               flights=flights,
                               dayOfFlight=dayLeave
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