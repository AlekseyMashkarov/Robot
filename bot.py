# Импорт компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from handlers import sms, get_anecdote, get_location, get_contact, parrot





# Функция main() для соединения с платформой Telegram
def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) # Обработчик команды /start
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms)) # обрабатываем текст кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote)) # обрабатываем текст кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact)) #Обработчик полученных контактов
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))  # Обработчик полученных геоданных
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) #Обработчик текстового сообщения

    my_bot.start_polling() # Проверка наличия сообщений платформы
    my_bot.idle()


# Запуск
if __name__ == "__main__":
    main()