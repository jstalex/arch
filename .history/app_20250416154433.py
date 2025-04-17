from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barber_name = db.Column(db.String(50), nullable=False)
    client_name = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)

@app.route('/add', methods=['POST'])
def add_order():
    barber_name = request.form.get('barber_name')
    client_name = request.form.get('client_name')
    order_date = request.form.get('order_date')
    new_order = Order(barber_name=barber_name, client_name=client_name, order_date=order_date)