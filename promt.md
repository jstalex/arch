есть вот такое задание и sql код описывающий структуру БД postgres.
Необходимо разработать информационную систему для отслеживания финансовых показателей работы парикмахерской. Парикмахерская обслуживает клиентов в соответствии с их пожеланиями и некоторым каталогом различных видов стрижки. Для каждой стрижки определены название, принадлежность полу (мужская, женская), стоимость работы. Каждый клиент заполняет анкету, указывая фамилию, имя, отчество, адрес электронной почты и контактный телефон. Некоторые клиенты могут перейти в категорию VIP и получить скидку. После того, как закончена очередная работа, документом фиксируются дата, стрижка, клиент и ФИО мастера.

CREATE TABLE haircuts (
    haircut_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT CHECK (gender IN ('male', 'female')),
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    is_vip BOOLEAN DEFAULT FALSE,
    discount DECIMAL(5, 2) CHECK (discount BETWEEN 0 AND 100) DEFAULT 0
);
CREATE TABLE barber (
    barber_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT
);
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    haircut_id INT REFERENCES haircuts(haircut_id) ON DELETE CASCADE,
    client_id INT REFERENCES clients(client_id) ON DELETE CASCADE,
    barber_id INT REFERENCES barbers(barber_id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

напиши простое веб приложение с использованием python. Должен быть графический интерфейс, который позволяет выводить данные из таблицы orders, добавлять их и удалять. Приложение должно запускаться в докер контейнере. БД postgres 16 будет запущена рядом в docker-compose

