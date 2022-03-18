import psycopg2
import telebot
import config
from telebot import types
import dbworker

bot = telebot.TeleBot(config.token)  # Создание бота с помощью токена

db_connection = psycopg2.connect(config.DB_URI, sslmode="require")  # Подключение у удалённоё базе данных
db_object = db_connection.cursor()

print("Старт бота")  # Вывод в отладочный чат, что бот работает


# Функция, вызываема при введении пользователем команды /start. Идёт обращение к базе дынных, и если пользователь не найден, создаётся новая запись
@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Пройти тестирование")

    markup.add(item)
    bot.send_message(message.chat.id,
                     f"Доброго времени суток, {username}!\nЯ бот, который задаст вас пару вопросов",
                     reply_markup=markup)
    # bot.send_sticker(message.chat.id, open('./media/Старт.jpg', 'rb'))
    
    db_object.execute(f"SELECT id FROM userbase WHERE id  = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute(
            "INSERT INTO userbase(id, users, counter,lastresult,stage,answers) VALUES (%s,%s,%s,%s,%s,%s)",
            (user_id, username, 0, "No turtle", 0, ""))
        db_connection.commit()

    dbworker.set_state(message.chat.id, config.States.S_ANS_1.value)


if __name__ == '__main__':
    bot.infinity_polling()
