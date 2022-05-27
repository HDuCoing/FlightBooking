from flask import render_template, url_for, redirect, request, flash
from flaskflights.models import LoginForm, RegistrationForm, User, FlightSelect, Aircraft
from flaskflights import app, db

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
    return render_template('register.html', form=form)

#todo make search work
@app.route('/book', methods=['GET', 'POST'])
def book():
    form = FlightSelect(request.form)
    # If user submits dates - take to listing of available flights in date range
    if request.method == 'POST':
        # specific date
        leave = form.leaveOn.data
        return_on = form.returnOn.data
        location = form.location.data
        
        # day of week - monday is 0 - sunday is 6
        dayLeave = leave.weekday()
        dayReturn = return_on.weekday()

        if dayLeave == 0: # if monday
            #if flyFrom == 'Dairy Flat':
            flights_available = [
                '8:00 A.M. Dairy Flat to Rotorua',
                '12 P.M. Rotorua to Dairy Flat',
            ]

        print("Location: " + location)
        print("Leave: " + str(dayLeave) + " Return: " + str(dayReturn))
        return render_template('flight_info.html')
    return render_template('book.html', form=form)
