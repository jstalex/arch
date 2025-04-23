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
                         email TEXT,
                         phone TEXT NOT NULL,
                         is_vip BOOLEAN DEFAULT FALSE,
                         discount DECIMAL(5, 2) CHECK (discount BETWEEN 0 AND 100) DEFAULT 0
);

CREATE TABLE barbers (
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

ALTER TABLE barbers ADD COLUMN experience INT;


INSERT INTO haircuts (name, gender, price) VALUES
                                               ('Мужская стрижка', 'male', 500.00),
                                               ('Женская стрижка', 'female', 700.00),
                                               ('Стрижка с укладкой', 'female', 800.00);

INSERT INTO clients (first_name, last_name, middle_name, email, phone, is_vip, discount) VALUES
                                                                                             ('Иван', 'Иванов', 'Иванович', 'ivanov@example.com', '1234567890', FALSE, NULL),
                                                                                             ('Мария', 'Петрова', 'Сергеевна', 'petrova@example.com', '0987654321', TRUE, 10.00),
                                                                                             ('Ольга', 'Сидорова', 'Александровна', 'sidorova@example.com', '1122334455', FALSE, NULL);

INSERT INTO barbers (first_name, last_name, middle_name, experience) VALUES
                                                                         ('Дмитрий', 'Смирнов', 'Викторович', 5),
                                                                         ('Анна', 'Кузнецова', 'Ивановна', 3),
                                                                         ('Алексей', 'Лебедев', 'Станиславович', 7);
                                                                        
INSERT INTO orders (haircut_id, client_id, barber_id, order_date)
VALUES (1, 1, 1, '2025-04-18 13:50:00.000000'),
       (2, 2, 2, '2025-04-17 13:50:00.000000'),
       (1, 3, 3, '2025-04-19 13:50:00.000000'),
       (2, 2, 2, '2025-04-17 13:50:00.000000'),
       (1, 3, 3, '2025-04-20 13:50:00.000000'),
       (2, 2, 2, '2025-04-21 13:50:00.000000'),
       (1, 3, 3, '2025-04-21 13:50:00.000000'),
       (2, 2, 2, '2025-04-22 13:50:00.000000'),
       (1, 3, 3, '2025-04-22 13:50:00.000000'),
       (3, 1, 2, '2025-04-22 13:50:00.000000');