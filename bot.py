# Импорт компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN, TG_API_URL
from bs4 import BeautifulSoup
import requests



# Функция sms() описывает логику обработки команды /start
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') # Сообщение в консоль
    my_keyboard = ReplyKeyboardMarkup([['Анекдот'], ['Начать']], resize_keyboard=True) # Добавлена кнопка
    bot.message.reply_text('Здравствуйте {}, я Робот! \nПоговорите со мной!'.format(bot.message.chat.first_name), reply_markup=my_keyboard)
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


# Функция main() для соединения с платформой Telgram
def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) # Обработчик команды /start
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms)) # обрабатываем текст кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote)) # обрабатываем текст кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) #Обработчик текстового сообщения

    my_bot.start_polling() # Проверка наличия сообщений платформы
    my_bot.idle()


# Запуск
main()