from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Database connection configuration
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'admin',
    'password': 'admin',
    'host': 'db',
    'port': '5432'
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Get orders with related data
    cur.execute("""
        SELECT o.order_id, h.name as haircut_name, c.first_name || ' ' || c.last_name as client_name,
               b.first_name || ' ' || b.last_name as barber_name, o.order_date
        FROM orders o
        JOIN haircuts h ON o.haircut_id = h.haircut_id
        JOIN clients c ON o.client_id = c.client_id
        JOIN barbers b ON o.barber_id = b.barber_id
        ORDER BY o.order_date DESC
    """)
    orders = cur.fetchall()
    
    # Get dropdown options
    cur.execute("SELECT haircut_id, name FROM haircuts")
    haircuts = cur.fetchall()
    
    cur.execute("SELECT client_id, first_name, last_name FROM clients")
    clients = cur.fetchall()
    
    cur.execute("SELECT barber_id, first_name, last_name FROM barbers")
    barbers = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('index.html', orders=orders, haircuts=haircuts, clients=clients, barbers=barbers)

@app.route('/add', methods=['POST'])
def add_order():
    haircut_id = request.form['haircut_id']
    client_id = request.form['client_id']
    barber_id = request.form['barber_id']
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO orders (haircut_id, client_id, barber_id) VALUES (%s, %s, %s)",
        (haircut_id, client_id, barber_id)
    )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:order_id>')
def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)