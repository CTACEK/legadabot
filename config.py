from enum import Enum

BOT_TOKEN = ""
DB_URI = ""


# Создание состояний по которым будет двигаться бот
class States(Enum):
    S_QSTN_1 = "1"
    S_QSTN_2 = "2"
    S_QSTN_3 = "3"
    S_QSTN_4 = "4"
    S_QSTN_5 = "5"
    S_QSTN_5 = "6"
    S_STATS = "7"
