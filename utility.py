from telegram import ReplyKeyboardMarkup, KeyboardButton


# Функция создаёт клавиатуру и её разметку
def get_keyboard():
    contact_button = KeyboardButton('Отправить контакты', request_contact=True)
    location_button = KeyboardButton('Отправить геопозицию', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([['Анекдот'], ['Начать'],
                                      [contact_button, location_button],
                                       ['Заполнить анкету']
                                       ], resize_keyboard=True)  # Добавлена кнопка
    return my_keyboard