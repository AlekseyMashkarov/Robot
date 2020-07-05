# Импорт компонентов
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
from handlers import *
import logging

# Настройки логгирования (Дата и время события, уровень важности, сообщение; Получение информационного события, Файл для записи логов)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


# Функция main() для соединения с платформой Telegram
def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    logging.info('Start bot')
    my_bot.dispatcher.add_handler(CommandHandler('start', sms)) # Обработчик команды /start
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Картинки'), send_meme)) # Кнопка отправки картинки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms)) # обрабатываем текст кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote)) # обрабатываем текст кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact)) #Обработчик полученных контактов
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))  # Обработчик полученных геоданных
    my_bot.dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex('Заполнить анкету'), anketa_start)],
                                                      states={
                                                          "user_name": [MessageHandler(Filters.text, anketa_get_name)],
                                                          "user_age": [MessageHandler(Filters.text, anketa_get_age)],
                                                          "evaluation": [MessageHandler(Filters.regex('1|2|3|4|5'), anketa_get_evaluation)],
                                                          "comment": [MessageHandler(Filters.regex('Пропустить'), anketa_exit_comment),
                                                                      MessageHandler(Filters.text, anketa_comment)]
                                                      },
                                                      fallbacks=[MessageHandler(
                                                          Filters.text | Filters.video | Filters.photo | Filters.document, dontknow)]
                                                      )
                                  )
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot)) #Обработчик текстового сообщения

    my_bot.start_polling() # Проверка наличия сообщений платформы
    my_bot.idle()


# Запуск
if __name__ == "__main__":
    main()