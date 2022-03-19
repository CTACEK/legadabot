import psycopg2
import config

db_connection = psycopg2.connect(config.DB_URI,  sslmode="require")
db_object = db_connection.cursor()


# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    db_object.execute(f"UPDATE users SET state = '{value}' WHERE id = '{user_id}'")
    db_connection.commit()

# Получаем текущее состояние
def get_current_state(user_id):
    db_object.execute(f"SELECT state from users WHERE id = '{user_id}'")
    result = db_object.fetchall()
    return str(result)[3]

#Добавляем текущий ответ пользователя
def add_answer(user_id, сategory, value):
    db_object.execute(f"UPDATE users SET {сategory} = '{value}' WHERE id = '{user_id}'")
    db_connection.commit()