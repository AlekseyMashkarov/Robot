from utility import get_keyboard
from bs4 import BeautifulSoup
import requests


# Функция sms() описывает логику обработки команды /start
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') # Сообщение в консоль
    bot.message.reply_text('Здравствуйте {}, я Робот! \nПоговорите со мной!'.format(bot.message.chat.first_name), reply_markup=get_keyboard())
    #print(bot.message)


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
