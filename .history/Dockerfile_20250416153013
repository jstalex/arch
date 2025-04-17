# Используйте официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальную часть кода приложения
COPY . .

# Указываем переменную окружения для Flask
ENV FLASK_APP=app.py

# Открываем порт, который будет использоваться приложением (по умолчанию 5000)
EXPOSE 5000

# Указываем команду для запуска приложения
CMD ["flask", "run", "--host=0.0.0.0"]