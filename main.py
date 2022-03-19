import psycopg2
import telebot
import config
import re
import db
from telebot import types
from qstnansw import *

bot = telebot.TeleBot(config.BOT_TOKEN)  # Создание бота с помощью токена

db_connection = psycopg2.connect(config.DB_URI, sslmode="require")  # Подключение у удалённоё базе данных
db_object = db_connection.cursor()

print("Старт бота")  # Вывод в отладочный чат, что бот работает


def createkeyboard(message, count):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if count == 1:
        item1 = types.KeyboardButton("1")
        markup.add(item1)
    elif count == 2:
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        markup.add(item1, item2)
    elif count == 3:
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        markup.add(item1, item2, item3)
    elif count == 4:
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        item4 = types.KeyboardButton("4")
        markup.add(item1, item2, item3, item4)
    elif count == 5:
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        item4 = types.KeyboardButton("4")
        item5 = types.KeyboardButton("5")
        markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, "Введите один из предложенных ответов:", reply_markup=markup)


def checking(message, count):
    if message.text in answers[:count]:
        return True
    else:
        bot.send_message(message.chat.id, f"Попробуйте ещё раз)")


def checksex(message):
    if message.text in ["М", "Ж", "Не важно"]:
        return True
    else:
        bot.send_message(message.chat.id, f"Попробуйте ещё раз)")


def checksity(message):
    if re.fullmatch(r'\D+', message.text):
        return True
    else:
        bot.send_message(message.chat.id, f"Попробуйте ещё раз)")


def checkage(message):
    if re.fullmatch(r'\d{1,3}', message.text):
        return True
    else:
        bot.send_message(message.chat.id, f"Попробуйте ещё раз)")


# Функция, вызываема при введении пользователем команды /start. Идёт обращение к базе дынных, и если пользователь не найден, создаётся новая запись
@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Пройти тестирование")

    markup.add(item)
    bot.send_message(message.chat.id,
                     f"Доброго времени суток, участник опроса!\nЯ бот, который задаст вам пару вопросов",
                     reply_markup=markup)

    db_object.execute(f"SELECT id FROM users WHERE id  = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id) VALUES (%s)", (user_id))
        db_connection.commit()

    db.set_state(message.chat.id, config.States.S_QSTN_0.value)


# Сброс предыдущих ответов, создание клавиатуры и задание первого вопроса + переход на новое состояние
@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_0.value)
def first_question(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("М")
    item2 = types.KeyboardButton("Ж")
    item3 = types.KeyboardButton("Не важно")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))], reply_markup=markup)

    db.set_state(message.chat.id, config.States.S_QSTN_1.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_1.value)
def second_question(message):
    if checksex(message):
        db.add_answer(message.chat.id, 'ans_1', message.text)
        bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))])
        db.set_state(message.chat.id, config.States.S_QSTN_2.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_2.value)
def second_question(message):
    if checkage(message):
        db.add_answer(message.chat.id, "ans_2", message.text)
        bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))])
        db.set_state(message.chat.id, config.States.S_QSTN_3.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_3.value)
def second_question(message):
    if checksity(message):
        db.add_answer(message.chat.id, "ans_3", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        createkeyboard(message, 5)
        db.set_state(message.chat.id, config.States.S_QSTN_4.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_4.value)
def third_question(message):
    if checking(message, 5):
        db.add_answer(message.chat.id, "ans_4", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        createkeyboard(message, 3)
        db.set_state(message.chat.id, config.States.S_QSTN_5.value)


# Отлавливаем ответ на 1 вопрос, проверяем его на корректность + задаём следующий вопрос и переходим на новое состояние
@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_5.value)
def second_question(message):
    if checking(message, 3):
        db.add_answer(message.chat.id, "ans_5", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        # bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][1])
        createkeyboard(message, 3)
        db.set_state(message.chat.id, config.States.S_QSTN_6.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_6.value)
def second_question(message):
    if checking(message, 3):
        db.add_answer(message.chat.id, "ans_6", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        createkeyboard(message, 3)
        db.set_state(message.chat.id, config.States.S_QSTN_7.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_7.value)
def second_question(message):
    if checking(message, 3):
        db.add_answer(message.chat.id, "ans_7", message.text)
        bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))])
        db.set_state(message.chat.id, config.States.S_QSTN_8.value)

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_8.value)
def second_question(message):
    db.add_answer(message.chat.id, "ans_8", message.text)
    bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))])
    db.set_state(message.chat.id, config.States.S_QSTN_9.value)

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_9.value)
def second_question(message):
    db.add_answer(message.chat.id, "ans_9", message.text)
    bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))])
    db.set_state(message.chat.id, config.States.S_STATS.value)

@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_STATS)
def second_question(message):
    bot.send_message(message.chat.id, )
    db.set_state(message.chat.id, config.States.S_STATS.value)


if __name__ == '__main__':
    bot.infinity_polling()
