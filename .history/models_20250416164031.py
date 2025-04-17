from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'  # Используйте название таблицы "orders"
    id = db.Column(db.Integer, primary_key=True)
    barber_name = db.Column(db.String(50), nullable=False)
    client_name = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.Date, nullable=False)