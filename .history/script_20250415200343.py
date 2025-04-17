# Установка необходимых библиотек (при необходимости)
!pip install psycopg2 matplotlib pandas

import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Задайте параметры соединения
conn_params = {
    'database': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',  # или другой адрес
    'port': '5432'
}

def fetch_orders():
    with psycopg2.connect(**conn_params) as conn:
        df = pd.read_sql_query("SELECT * FROM orders", conn)
    return df

def add_order(order_info):
    with psycopg2.connect(**conn_params) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO orders (haircut_id, client_id, barber_id) 
            VALUES (%s, %s, %s)
            """,
            (order_info['haircut_id'], order_info['client_id'], order_info['barber_id'])
        )
        conn.commit()
        messagebox.showinfo("Информация", "Заказ добавлен успешно!")
        refresh_orders()

def delete_order(order_id):
    with psycopg2.connect(**conn_params) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()
        messagebox.showinfo("Информация", "Заказ удален успешно!")
        refresh_orders()

def refresh_orders():
    for row in tree.get_children():
        tree.delete(row)
    orders = fetch_orders()
    for _, order in orders.iterrows():
        tree.insert("", "end", values=order)

def plot_orders_distribution():
    with psycopg2.connect(**conn_params) as conn:
        df = pd.read_sql_query(
            """
            SELECT b.first_name, b.last_name, COUNT(o.order_id) AS order_count
            FROM orders o
            JOIN barbers b ON o.barber_id = b.barber_id
            GROUP BY b.barber_id
            """, 
            conn
        )
    
    plt.figure(figsize=(10, 5))
    plt.bar(df['first_name'] + ' ' + df['last_name'], df['order_count'], color='skyblue')
    plt.xlabel('Барберы')
    plt.ylabel('Количество заказов')
    plt.title('Распределение заказов по барберам')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Основное окно приложения
root = tk.Tk()
root.title("Управление заказами")

# Настройка таблицы для отображения заказов
tree = ttk.Treeview(root, columns=("order_id", "haircut_id", "client_id", "barber_id", "order_date"), show='headings')
tree.heading("order_id", text="ID заказа")
tree.heading("haircut_id", text="ID стрижки")
tree.heading("client_id", text="ID клиента")
tree.heading("barber_id", text="ID барбера")
tree.heading("order_date", text="Дата заказа")
tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Кнопка для обновления данных
refresh_button = tk.Button(root, text="Обновить данные", command=refresh_orders)
refresh_button.pack(side=tk.TOP)

# Кнопка для добавления заказа
def open_add_order_window():
    add_window = tk.Toplevel(root)
    add_window.title("Добавить заказ")

    tk.Label(add_window, text="ID стрижки:").grid(row=0, column=0)
    haircut_id_entry = tk.Entry(add_window)
    haircut_id_entry.grid(row=0, column=1)

    tk.Label(add_window, text="ID клиента:").grid(row=1, column=0)
    client_id_entry = tk.Entry(add_window)
    client_id_entry.grid(row=1, column=1)

     tk.Label(add_window, text="ID барбера:").grid(row=2, column=0)
    barber_id_entry = tk.Entry(add_window)
    barber_id_entry.grid(row=2, column=1)

    def add_order_action():
        order_info = {
            'haircut_id': haircut_id_entry.get(),
            'client_id': client_id_entry.get(),
            'barber_id': barber_id_entry.get()
        }
        add_order(order_info)
        add_window.destroy()

    add_button = tk.Button(add_window, text="Добавить заказ", command=add_order_action)
    add_button.grid(row=3, columnspan=2)

add_order_button = tk.Button(root, text="Добавить заказ", command=open_add_order_window)
add_order_button.pack(side=tk.TOP)

# Кнопка для удаления заказа
def open_delete_order_window():
    delete_window = tk.Toplevel(root)
    delete_window.title("Удалить заказ")

    tk.Label(delete_window, text="ID заказа:").grid(row=0, column=0)
    order_id_entry = tk.Entry(delete_window)
    order_id_entry.grid(row=0, column=1)

    def delete_order_action():
        order_id = order_id_entry.get()
        delete_order(order_id)
        delete_window.destroy()

    delete_button = tk.Button(delete_window, text="Удалить заказ", command=delete_order_action)
    delete_button.grid(row=1, columnspan=2)

delete_order_button = tk.Button(root, text="Удалить заказ", command=open_delete_order_window)
delete_order_button.pack(side=tk.TOP)

# Кнопка для построения гистограммы
plot_button = tk.Button(root, text="Построить гистограмму", command=plot_orders_distribution)
plot_button.pack(side=tk.TOP)

# Начальная загрузка данных
refresh_orders()

# Запуск главного цикла приложения
root.mainloop()