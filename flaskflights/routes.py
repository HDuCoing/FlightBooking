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

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        flash('Thanks for registering with AirDuCoing!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = FlightSelect
    return render_template('book.html', form=form)

