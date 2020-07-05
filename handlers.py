from utility import get_keyboard
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
import requests
from glob import glob
from random import choice


# Функция sms() описывает логику обработки команды /start
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') # Сообщение в консоль
    bot.message.reply_text('Здравствуйте {}, я Робот! \nПоговорите со мной!'.format(bot.message.chat.first_name), reply_markup=get_keyboard())
    #print(bot.message)


# функция отправляет случайную картинку
def send_meme(bot, update):
    lists = glob('images/*')  # создаем список из названий картинок
    picture = choice(lists)  # берем из списка одну картинку
    update.bot.send_photo(chat_id=bot.message.chat.id, photo=open(picture, 'rb'))  # отправляем картинку


# Функция Анекдот
def get_anecdote(bot, update):
    recieve = requests.get('http://anekdotme.ru/random') # запрос к странице
    page = BeautifulSoup(recieve.text, "html.parser") # подключаем хтмл парсер, получаем текст страницы
    find = page.select('.anekdot_text') # из страницы html получаем class="anekdot_text"
    for text in find:
        page = (text.getText().strip()) # из class="anekdot_text" получаем текст и убираем пробелы по сторонам
    bot.message.reply_text(page) # отправляем анекдот, последний


# Функция parrot() отвечает тем же сообщением, которое ему прислали
def parrot(bot, update):
    print(bot.message.text) # печать в консоль принятого сообщения
    bot.message.reply_text(bot.message.text) # отправляем обратно текст


# Функция печатает и отвечает на полученный контакт
def get_contact(bot, update):
    print(bot.message.contact)
    bot.message.reply_text('{}, мы получили ваш номер телефона!'.format(bot.message.chat.first_name))


# Функция печатает и отвечает на полученные геоданные
def get_location(bot, update):
    print(bot.message.location)
    bot.message.reply_text('{}, мы получили ваше местоположение!'.format(bot.message.chat.first_name))


# Функция Анкета
def anketa_start(bot, update):
    bot.message.reply_text('Как вас зовут?', reply_markup=ReplyKeyboardRemove())  # вопрос и убираем основную клавиатуру
    return "user_name"  # ключ для определения следующего шага


def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text  # временно сохраняем ответ
    bot.message.reply_text("Сколько вам лет?")  # задаем вопрос
    return "user_age"  # ключ для определения следующего шага


def anketa_get_age(bot, update):
    update.user_data['age'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [["1", "2", "3", "4", "5"]]  # создаем клавиатуру
    bot.message.reply_text(
        "Оцените статью от 1 до 5",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=True))  # при нажатии клавиатура исчезает
    return "evaluation"  # ключ для определения следующего шага


def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text  # временно сохраняем ответ
    reply_keyboard = [["Пропустить"]]  # создаем клавиатуру
    bot.message.reply_text("Напишите отзыв или нажмите кнопку пропустить этот шаг.",
                           reply_markup=ReplyKeyboardMarkup(
                               reply_keyboard, resize_keyboard=True, one_time_keyboard=True))  # клава исчезает
    return "comment"  # ключ для определения следующего шага


def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text  # временно сохраняем ответ
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}
    <b>Комментарий:</b> {comment}
    """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text("Спасибо вам за комментарий!", reply_markup=get_keyboard())  # сообщение и возвр. осн. клаву
    return ConversationHandler.END  # выходим из диалога


def anketa_exit_comment(bot, update):
    text = """Результат опроса:
    <b>Имя:</b> {name}
    <b>Возраст:</b> {age}
    <b>Оценка:</b> {evaluation}""".format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)  # текстовое сообщение с форматированием HTML
    bot.message.reply_text("Спасибо!", reply_markup=get_keyboard())  # отправляем сообщение и возвращаем осн. клаву
    return ConversationHandler.END  # выходим из диалога


def dontknow(bot, update):
    bot.message.reply_text("Я вас не понимаю, выберите оценку на клавиатуре!")

