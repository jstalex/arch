from flask import Flask, render_template, request, redirect, url_for
from models import db, Order
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    orders = Order.query.all()
    return render_template('index.html', orders=orders)

@app.route('/add', methods=['POST'])
def add_order():
    barber_name = request.form['barber_name']
    client_name = request.form['client_name']
    order_date = request.form['order_date']
    new_order = Order(barber_name=barber_name, client_name=client_name, order_date=order_date)
    
    db.session.add(new_order)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_order(id):
    order = Order.query.get(id)
    if order:
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/histogram')
def histogram():
    orders = Order.query.all()
    barber_counts = {}
    
    for order in orders:
        if order.barber_name in barber_counts:
            barber_counts[order.barber_name] += 1
        else:
            barber_counts[order.barber_name] = 1
    
    # Создание гистограммы
    plt.figure(figsize=(10, 6))
    plt.bar(barber_counts.keys(), barber_counts.values(), color='blue')
    plt.xlabel('Барберы')
    plt.ylabel('Количество заказов')
    plt.title('Количество заказов по барберам')
    plt.xticks(rotation=45)
    
    # Сохранение изображения
    plt.savefig('static/plot.png')
    plt.close()

    return render_template('histogram.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создаем все таблицы при старте
    app.run(debug=True)