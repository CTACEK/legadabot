import psycopg2
import telebot
import config
import re
import db
import matplotlib.pyplot as plt
from telebot import types
from qstnansw import *

bot = telebot.TeleBot(config.BOT_TOKEN)  # Создание бота с помощью токена

db_connection = psycopg2.connect(config.DB_URI, sslmode="require")  # Подключение у удалённоё базе данных
db_object = db_connection.cursor()

print("Старт бота")  # Вывод в отладочный чат, что бот работает


def createkeyboard(message, count):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("1")
    item2 = types.KeyboardButton("2")
    item3 = types.KeyboardButton("3")
    item4 = types.KeyboardButton("4")
    item5 = types.KeyboardButton("5")
    if count == 1:
        markup.add(item1)
    elif count == 2:
        markup.add(item1, item2)
    elif count == 3:
        markup.add(item1, item2, item3)
    elif count == 4:
        markup.add(item1, item2, item3, item4)
    elif count == 5:
        markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, "Введите один из предложенных ответов:", reply_markup=markup)


def creategraph_for_numberedans(num_qst, criteria):
    if criteria == "Нет":
        fig, axes = plt.subplots(figsize=(9, 9))
        labels = [ans[3:] for ans in questions[num_qst][1].split('\n')]
        all_data = db.get_data_2(num_qst, len(labels), criteria)

        real = [ans for ans in labels if all_data[str(labels.index(ans) + 1)] != 0]
        curr_data = [value for value in all_data.values() if value != 0]

        axes.pie(curr_data, labels=real, autopct='%1.1f%%', startangle=130)
        axes.axis("equal")
        axes.set_title(f'{questions[num_qst][0]}')
    elif criteria == "Пол":
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 4))

        labels = [ans[3:] for ans in questions[num_qst][1].split('\n')]
        all_data_m, all_data_w = db.get_data_2(num_qst, len(labels), criteria)

        real_m = [ans for ans in labels if all_data_m[str(labels.index(ans) + 1)] != 0]
        curr_data_m = [value for value in all_data_m.values() if value != 0]

        real_w = [ans for ans in labels if all_data_w[str(labels.index(ans) + 1)] != 0]
        curr_data_w = [value for value in all_data_w.values() if value != 0]

        ax1.pie(curr_data_m, labels=real_m, autopct='%1.1f%%', startangle=130)
        ax1.set_title('Как отвечали мужчины')
        ax2.pie(curr_data_w, labels=real_w, autopct='%1.1f%%', startangle=130)
        ax2.set_title('Как отвечали женщины')
    elif criteria == "Возраст":
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))
        labels = [ans[3:] for ans in questions[num_qst][1].split('\n')]

        all_data_29, all_data_30, all_data_50 = db.get_data_2(num_qst, len(labels), criteria)

        real_29 = [ans for ans in labels if all_data_29[str(labels.index(ans) + 1)] != 0]
        curr_data_29 = [value for value in all_data_29.values() if value != 0]

        real_30 = [ans for ans in labels if all_data_30[str(labels.index(ans) + 1)] != 0]
        curr_data_30 = [value for value in all_data_30.values() if value != 0]

        real_50 = [ans for ans in labels if all_data_50[str(labels.index(ans) + 1)] != 0]
        curr_data_50 = [value for value in all_data_50.values() if value != 0]

        ax1.pie(curr_data_29, labels=real_29, autopct='%1.1f%%', startangle=130)
        ax1.set_title('Как отвечали люди до 29 лет')
        ax2.pie(curr_data_30, labels=real_30, autopct='%1.1f%%', startangle=130)
        ax2.set_title('Как отвечали люди от 30 до 50 лет')
        ax3.pie(curr_data_50, labels=real_50, autopct='%1.1f%%', startangle=130)
        ax3.set_title('Как отвечали люди больше 50 лет')
    elif criteria == "Образование":
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=1, ncols=5, figsize=(30, 5))
        labels = [ans[3:] for ans in questions[num_qst][1].split('\n')]

        all_data_1, all_data_2, all_data_3, all_data_4, all_data_5 = db.get_data_2(num_qst, len(labels), criteria)

        real_1 = [ans for ans in labels if all_data_1[str(labels.index(ans) + 1)] != 0]
        curr_data_1 = [value for value in all_data_1.values() if value != 0]

        real_2 = [ans for ans in labels if all_data_2[str(labels.index(ans) + 1)] != 0]
        curr_data_2 = [value for value in all_data_2.values() if value != 0]

        real_3 = [ans for ans in labels if all_data_3[str(labels.index(ans) + 1)] != 0]
        curr_data_3 = [value for value in all_data_3.values() if value != 0]

        real_4 = [ans for ans in labels if all_data_4[str(labels.index(ans) + 1)] != 0]
        curr_data_4 = [value for value in all_data_4.values() if value != 0]

        real_5 = [ans for ans in labels if all_data_5[str(labels.index(ans) + 1)] != 0]
        curr_data_5 = [value for value in all_data_5.values() if value != 0]

        ax1.pie(curr_data_1, labels=real_1, autopct='%1.1f%%', startangle=130)
        ax1.set_title('Как отвечали люди c основным общим образованием')
        ax2.pie(curr_data_2, labels=real_2, autopct='%1.1f%%', startangle=130)
        ax2.set_title('Как отвечали люди с средним общим образованием')
        ax3.pie(curr_data_3, labels=real_3, autopct='%1.1f%%', startangle=130)
        ax3.set_title('Как отвечали люди с средним профессиональным')
        ax4.pie(curr_data_4, labels=real_4, autopct='%1.1f%%', startangle=130)
        ax4.set_title('Как отвечали люди с неоконченным высшим')
        ax5.pie(curr_data_5, labels=real_5, autopct='%1.1f%%', startangle=130)
        ax5.set_title('Как отвечали люди с высшим образованием')

    fig.savefig(f'./resources/photo/graphquestion{num_qst}.png')


def checking(message, count):
    if message.text in answers[:count]:
        return True
    else:
        bot.send_message(message.chat.id, f"Попробуйте ещё раз)")


def checksex(message):
    if message.text in ["М", "Ж"]:
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
    user_id = int(message.from_user.id)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Пройти тестирование")

    markup.add(item)
    bot.send_message(message.chat.id,
                     f"Доброго времени суток, участник опроса!\nЯ бот, который задаст вам пару вопросов",
                     reply_markup=markup)

    db_object.execute(f"SELECT id FROM users WHERE id  = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id) VALUES (%s)", (user_id,))
        db_connection.commit()

    db.set_state(message.chat.id, config.States.S_QSTN_0.value)


# Функция, вызываемая при введении пользователем команды /reset. Идёт перемещение на меню перепрохождения теста
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Да!")
    markup.add(item1)
    bot.send_message(message.chat.id, "Начинаем?", reply_markup=markup)
    db.set_state(message.chat.id, config.States.S_QSTN_0.value)


@bot.message_handler(commands=["stats"])
def get_stats(message):
    ask1, ask2, ask3 = 4, 5, 6
    creategraph_for_numberedans(ask1, "Пол")
    bot.send_message(message.chat.id, f"Статистика на вопрос: {questions[ask1][0]}")
    bot.send_photo(message.chat.id, open(f'./resources/photo/graphquestion{ask1}.png', 'rb'))

    creategraph_for_numberedans(ask2, "Возраст")
    bot.send_message(message.chat.id, f"Статистика на вопрос: {questions[ask2][0]}")
    bot.send_photo(message.chat.id, open(f'./resources/photo/graphquestion{ask2}.png', 'rb'))

    creategraph_for_numberedans(ask3, "Образование")
    bot.send_message(message.chat.id, f"Статистика на вопрос: {questions[ask3][0]}")
    bot.send_photo(message.chat.id, open(f'./resources/photo/graphquestion{ask3}.png', 'rb'))


# Сброс предыдущих ответов, создание клавиатуры и задание первого вопроса + переход на новое состояние
@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_0.value)
def first_question(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("М")
    item2 = types.KeyboardButton("Ж")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))], reply_markup=markup)

    db.set_state(message.chat.id, config.States.S_QSTN_1.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_1.value)
def second_question(message):
    if checksex(message):
        db.add_answer(message.chat.id, 'ans_1', message.text)
        bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))])
        db.set_state(message.chat.id, config.States.S_QSTN_2.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_2.value)
def third_question(message):
    if checkage(message):
        db.add_answer(message.chat.id, "ans_2", message.text)
        bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))])
        db.set_state(message.chat.id, config.States.S_QSTN_3.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_3.value)
def fourth_question(message):
    if checksity(message):
        db.add_answer(message.chat.id, "ans_3", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        createkeyboard(message, 5)
        db.set_state(message.chat.id, config.States.S_QSTN_4.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_4.value)
def fifth_question(message):
    if checking(message, 5):
        db.add_answer(message.chat.id, "ans_4", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        createkeyboard(message, 3)
        db.set_state(message.chat.id, config.States.S_QSTN_5.value)


# Отлавливаем ответ на 5 вопрос, проверяем его на корректность + задаём следующий вопрос и переходим на новое состояние
@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_5.value)
def sixth_question(message):
    if checking(message, 3):
        db.add_answer(message.chat.id, "ans_5", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        createkeyboard(message, 4)
        db.set_state(message.chat.id, config.States.S_QSTN_6.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_6.value)
def seven_question(message):
    if checking(message, 4):
        db.add_answer(message.chat.id, "ans_6", message.text)
        for i in range(2): bot.send_message(message.chat.id, questions[int(db.get_current_state(message.chat.id))][i])
        createkeyboard(message, 2)
        db.set_state(message.chat.id, config.States.S_QSTN_7.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_QSTN_7.value)
def eighth_question(message):
    if checking(message, 2):
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
    db.set_state(message.chat.id, config.States.S_CNGR.value)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_CNGR.value)
def second_question(message):
    db.add_answer(message.chat.id, "ans_10", message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/reset")
    item2 = types.KeyboardButton("/stats")
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     "Большое спасибо за участие в тесте\nЕсли хотите пройти тест ещё раз? - Тыкайке /reset\nНо а если вам интересно узнать статистику - Тыкайне /stats",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: db.get_current_state(message.chat.id) == config.States.S_LOBBY.value)
def eighth_question(message):
    if not message.text == "/reset" or not message.text == "/stats":
        bot.send_message(message.chat.id, "Простите, но у меня нет такой команды :с")


if __name__ == '__main__':
    bot.infinity_polling()
