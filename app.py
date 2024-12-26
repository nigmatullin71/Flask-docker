from flask import Flask, request
from datetime import datetime
import psycopg2 # type: ignore

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        dbname='counter_db',
        user='user',
        password='password',
        host='db',  # Имя контейнера базы данных из docker-compose.yml
        port='5432'
    )
    return conn

# Главная страница
@app.route('/')
def hello():
    client_info = request.headers.get('User-Agent')  # Получаем информацию о клиенте
    now = datetime.now()  # Текущее время

    # Сохраняем данные в базу данных
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO table_counter (datetime, client_info) VALUES (%s, %s);",
        (now, client_info)
    )
    conn.commit()
    cursor.close()
    conn.close()

    # Считаем количество запросов
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM table_counter;")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return f'Hello World! I have been seen {count} times.\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
