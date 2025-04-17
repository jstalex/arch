from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
        SELECT o.order_id, h.name as haircut_name, 
               c.first_name || ' ' || c.last_name as client_name,
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
    
    cur.execute("SELECT barber_id, first_name, last_name FROM barbers")
    barbers = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('index.html', orders=orders, haircuts=haircuts, barbers=barbers)

@app.route('/add', methods=['POST'])
def add_order():
    # Required fields
    haircut_id = request.form.get('haircut_id')
    barber_id = request.form.get('barber_id')
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    phone = request.form.get('phone', '').strip()
    
    # Validate required fields
    if not all([haircut_id, barber_id, first_name, last_name, phone]):
        flash('Пожалуйста, заполните все обязательные поля', 'error')
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Check if client exists
        cur.execute(
            "SELECT client_id FROM clients WHERE phone = %s",
            (phone,)
        )
        client = cur.fetchone()
        
        if not client:
            # Insert new client
            cur.execute(
                """INSERT INTO clients 
                (first_name, last_name, phone) 
                VALUES (%s, %s, %s) RETURNING client_id""",
                (first_name, last_name, phone)
            )
            client_id = cur.fetchone()[0]
            flash('Новый клиент успешно добавлен', 'info')
        else:
            client_id = client[0]
        
        # Insert order
        cur.execute(
            """INSERT INTO orders 
            (haircut_id, client_id, barber_id) 
            VALUES (%s, %s, %s)""",
            (haircut_id, client_id, barber_id)
        )
        
        conn.commit()
        flash('Заказ успешно добавлен', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка при добавлении заказа: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:order_id>')
def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()
        flash('Заказ успешно удален', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Ошибка при удалении заказа: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/get_report_data')
def get_report_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT b.first_name || ' ' || b.last_name as barber_name, COUNT(o.order_id) as orders_count
            FROM orders o
            JOIN barbers b ON o.barber_id = b.barber_id
            GROUP BY b.first_name, b.last_name
            ORDER BY orders_count DESC
        """)
        report_data = cur.fetchall()
        
        barbers = [row[0] for row in report_data]
        counts = [row[1] for row in report_data]
        
        # Создаем гистограмму
        plt.figure(figsize=(10, 6))
        bars = plt.bar(barbers, counts, color='#6d5b97')
        
        # Добавляем значения на столбцы
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    '%d' % int(height),
                    ha='center', va='bottom')
        
        plt.title('Количество заказов по мастерам')
        plt.xlabel('Мастера')
        plt.ylabel('Количество заказов')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Сохраняем график в буфер
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        # Кодируем изображение в base64
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        
        return jsonify({
            'status': 'success',
            'plot_url': plot_url,
            'data': report_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)