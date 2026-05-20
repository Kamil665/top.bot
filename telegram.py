import telebot
from telebot import types

bot = telebot.TeleBot('8717926440:AAERiHkHYR6cpT8OG9S0di0PwWaCKQ98_fM')

# глобальные переменные
name = ''
surname = ''
age = 0


# СТАРТ РЕГИСТРАЦИИ
@bot.message_handler(commands=['reg'])
def start(message):
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)


# ИМЯ
def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)


# ФАМИЛИЯ
def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)


# ВОЗРАСТ + КНОПКИ
def get_age(message):
    global age
    try:
        age = int(message.text)

        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_yes, key_no)

        question = f'Тебе {age} лет, тебя зовут {name} {surname}?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    except ValueError:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)


# ОБРАБОТКА КНОПОК
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global name, surname, age

    if call.data == "yes":
        # тут можно сохранить данные
        bot.send_message(call.message.chat.id, 'Запомню :)')

    elif call.data == "no":
        # очищаем данные
        name = ''
        surname = ''
        age = 0

        # начинаем заново
        bot.send_message(call.message.chat.id, "Давай попробуем ещё раз.\nКак тебя зовут?")
        bot.register_next_step_handler(call.message, get_name)


# ЗАПУСК БОТА
bot.polling(none_stop=True)