# Импорт компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL



# Функция sms() описывает логику обработки команды /start
def sms(bot, update):
    print('Кто-то отправил команду /start. Что мне делать?') # Сообщение в консоль
    bot.message.reply_text('Здравствуйте {}, я Робот! \nПоговорите со мной!'.format(bot.message.chat.first_name))
    #print(bot.message)


# Функция parrot() отвечает тем же сообщением, которое ему прислали
def parrot(bot, update):
    print(bot.message.text) # печать в консоль принятого сообщения
    bot.message.reply_text(bot.message.text) # отправляем обратно текст

# Функция main() для соединения с платформой Telgram
def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) # Обработчик команды /start
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) #Обработчик текстового сообщения

    my_bot.start_polling() # Проверка наличия сообщений платформы
    my_bot.idle()


# Запуск
main()