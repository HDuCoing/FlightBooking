from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='templates')

app.config['SECRET_KEY'] = '988e33e178a964ca1da479bd8b22dc3e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


from flaskflights import routes