from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://db:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Appointment


@app.route('/')
def index():
    appointments = Appointment.query.all()
    return render_template('index.html', appointments=appointments)


@app.route('/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        new_appointment = Appointment(name=name, date=date, time=time)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_appointment.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if request.method == 'POST':
        appointment.name = request.form['name']
        appointment.date = request.form['date']
        appointment.time = request.form['time']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_appointment.html', appointment=appointment)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()  # Создание таблицы в базе данных
    app.run(debug=True)