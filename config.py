from enum import Enum
import telebot
from telebot import types
token = '1247164599:AAGwb4xb2KN3YgKLO37lwZZTtddcG-dz_T0'
bot = telebot.TeleBot(token, threaded=False)
db_file = 'marathon_bot.vdb'
admin_db_file = 'admin_bot.vdb'
tag_file = 'currenttag.vdb'
class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_USERNAME = "1" # ввод username
    S_ENTER_FOLLOW = "2"
    S_SEND_PIC = "3"
class AdminStates(Enum):
    S_START = "0"  # Начало нового диалога
    S_ENTER_TODO = "1" # ввод username
    S_ENTER_NEWM = "2" # ввод тега для нового марафона
    S_ENTER_FOLLOWLIST = "3" # ввод списка подписок для марафона
    S_ENTER_BONUSDOC = "4" # отправка бонусного файла
    S_ENTER_BONUSPIC = "5" # отправка бонусного фото
    S_ENTER_BONUSTEXT = "6" # отправка бонусного текста
    S_ENTER_SHOWTAG = "7" # отправка тега для проверки инфо
    S_ENTER_SHOW = "8" # отправка инфо о марафоне
    S_ENTER_OLD = "9" # изменение существуещего марафона

keyboard = types.InlineKeyboardMarkup(row_width = 1)
keyboard.add(*[types.InlineKeyboardButton(text="Изменить данные существуещего марафона", callback_data="old"),\
        types.InlineKeyboardButton(text="Ввести тег и создать новый марафон", callback_data="new"),\
        types.InlineKeyboardButton(text="Проверить подписки у пользователя", callback_data="check"),\
        types.InlineKeyboardButton(text="Просмотреть инфо о марафоне", callback_data="show")])

new_key = types.InlineKeyboardMarkup(row_width = 1)
new_key.add(*[types.InlineKeyboardButton(text="Добавить список аккаунтов, на которые проверяется подписка", callback_data="new_follow"),\
        types.InlineKeyboardButton(text="Добавить бонус(файл)", callback_data="bonus"),\
        types.InlineKeyboardButton(text="Просмотреть инфо о марафоне", callback_data="show")])

change_key = types.InlineKeyboardMarkup(row_width = 1)
change_key.add(*[types.InlineKeyboardButton(text="Изменить список аккаунтов, на которые проверяется подписка", callback_data="new_follow"),\
        types.InlineKeyboardButton(text="Изменить бонус(файл)", callback_data="bonus"),\
        types.InlineKeyboardButton(text="Просмотреть инфо о марафоне", callback_data="show")])

after_follow_key = types.InlineKeyboardMarkup(row_width = 1)
after_follow_key.add(*[types.InlineKeyboardButton(text="Ввести новый список аккаунтов, на которые проверяется подписка", callback_data="new_follow"),\
        types.InlineKeyboardButton(text="Добавить бонус(файл)", callback_data="bonus"),\
        types.InlineKeyboardButton(text="Просмотреть инфо о марафоне", callback_data="show"),\
        types.InlineKeyboardButton(text="Перейти в начало", callback_data="reset") ])

bonus_types = types.InlineKeyboardMarkup(row_width = 1)
bonus_types.add(*[types.InlineKeyboardButton(text="файловый документ (pdf, docx и тп)", callback_data="document"),\
        types.InlineKeyboardButton(text="фото", callback_data="photo"),types.InlineKeyboardButton(text="описание бонусного файла/текст", callback_data="text")])

after_file_key = types.InlineKeyboardMarkup(row_width = 1)
after_file_key.add(*[types.InlineKeyboardButton(text="Добавить описание к файлу", callback_data="text"),\
        types.InlineKeyboardButton(text="Просмотреть инфо о марафоне", callback_data="show"),\
        types.InlineKeyboardButton(text="Перейти в начало", callback_data="reset") ])

after_bonus_key = types.InlineKeyboardMarkup(row_width = 1)
after_bonus_key.add(*[types.InlineKeyboardButton(text="Ввести новый список аккаунтов, на которые проверяется подписка", callback_data="new_follow"),\
        types.InlineKeyboardButton(text="Изменить бонус(файл)", callback_data="bonus"),\
        types.InlineKeyboardButton(text="Просмотреть инфо о марафоне", callback_data="show"),\
        types.InlineKeyboardButton(text="Перейти в начало", callback_data="reset") ])
