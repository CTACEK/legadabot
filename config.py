from enum import Enum

BOT_TOKEN = "5185285412:AAHrKwxdQwpLN_kGTGsN2trFPuL6e3HPJ84"
DB_URI = "postgres://xnslxucxorkwwk:9d889a744072a52ec027d59af5b26bd55b13a173ebcd44dc9e63276841ebb60f@ec2-63-34-223-144.eu-west-1.compute.amazonaws.com:5432/dc9ocpmtrg9pqs"


# Создание состояний по которым будет двигаться бот
class States(Enum):
    S_QSTN_0 = "0"
    S_QSTN_1 = "1"
    S_QSTN_2 = "2"
    S_QSTN_3 = "3"
    S_QSTN_4 = "4"
    S_QSTN_5 = "5"
    S_QSTN_6 = "6"
    S_QSTN_7 = "7"
    S_QSTN_8 = "8"
    S_QSTN_9 = "9"
    S_QSTN_10 = "10"
    S_STATS = "11"
