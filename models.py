from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'  # Указываем название таблицы

    order_id = db.Column(db.Integer, primary_key=True)  # Поле для ID заказа
    haircut_id = db.Column(db.Integer, db.ForeignKey('haircuts.haircut_id'), nullable=False)  # Ссылка на таблицу haircuts
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'), nullable=False)  # Ссылка на таблицу clients
    barber_id = db.Column(db.Integer, db.ForeignKey('barbers.barber_id'), nullable=False)  # Ссылка на таблицу barbers
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)  # Дата заказа

    # Опционально: связи с другими моделями
    haircut = db.relationship('Haircut', backref='orders', lazy=True)
    client = db.relationship('Client', backref='orders', lazy=True)
    barber = db.relationship('Barber', backref='orders', lazy=True)

    def __repr__(self):
        return f'<Order {self.order_id}>'