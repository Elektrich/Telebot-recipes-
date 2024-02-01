import telebot
from telebot import types
import time
import kor_, tor_
import variables as var

# токен бота
TOKEN = "6518544830:AAFYaLYYFUxAU3-KfKtJZtyTRCikr8oRYbQ"
bot = telebot.TeleBot(TOKEN)

name = bot.get_my_name()


# команда старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, я {name.name} - бот, умеющий искать рецепты")
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Да", callback_data="yes")
    button2 = types.InlineKeyboardButton("Нет", callback_data="no")
    markup.add(button1, button2)

    bot.send_message(message.chat.id, f"Хочешь найти какой-нибудь рецепт, {message.from_user.first_name}?",
                     reply_markup=markup)


def katalog_of_resipes(message):
    kor_.katalog_of_resipes(message)


def text_of_resipe(req):
    tor_.text_of_recipe(req)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback(callback):
    if callback.data == 'yes':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Gastronom", callback_data="gastr")
        button2 = types.InlineKeyboardButton("Art-Lunch", callback_data="art")
        markup.add(button1, button2)
        bot.send_message(callback.message.chat.id, f"Выбери сайт, с которого будешь искать рецепт", reply_markup=markup)

    elif callback.data == "gastr":
        if var.work:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Да", callback_data="not")
            button2 = types.InlineKeyboardButton("Нет", callback_data="no")
            markup.add(button1, button2)
            bot.send_message(callback.message.chat.id, "Не спамь!!! Могу только перезапустить.Надо?", reply_markup=markup)

        else:
            var.work = True
            var.site = "Gastronom"
            bot.send_message(callback.message.chat.id, "Нипиши рецепт, который хочешь найти")
            bot.register_next_step_handler(callback.message, katalog_of_resipes)

    elif callback.data == "art":
        if var.work:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Да", callback_data="not")
            button2 = types.InlineKeyboardButton("Нет", callback_data="no")
            markup.add(button1, button2)
            bot.send_message(callback.message.chat.id, "Не спамь!!! Могу только перезапустить.Надо?", reply_markup=markup)
        else:
            var.work = True
            var.site = "Art-Lunch"
            bot.send_message(callback.message.chat.id, "Нипиши рецепт, который хочешь найти")
            bot.register_next_step_handler(callback.message, katalog_of_resipes)

    elif callback.data == 'no':
        bot.send_message(callback.message.chat.id, f"Как хочешь")

    elif callback.data == 'yea':
        if var.work_second_part:

            markup_2 = types.InlineKeyboardMarkup()

            button1 = types.InlineKeyboardButton("Да", callback_data="not")
            button2 = types.InlineKeyboardButton("Нет", callback_data="no")
            markup_2.add(button1, button2)
            bot.send_message(callback.message.chat.id, "Не спамь!!! Могу только перезапустить.Надо?", reply_markup=markup_2)
        else:
            var.work_second_part = True
            bot.send_message(callback.message.chat.id, f"Напиши рецепт, который тебе понравился")
            bot.register_next_step_handler(callback.message, text_of_resipe)

    elif callback.data == 'not':
        var.work = False
        var.work_second_part = False
        bot.send_message(callback.message.chat.id, f"Хорошо, я перезапущу")
        time.sleep(0.5)
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Gastronom", callback_data="gastr")
        button2 = types.InlineKeyboardButton("Art-Lunch", callback_data="art")
        markup.add(button1, button2)
        bot.send_message(callback.message.chat.id, f"Выбери сайт, с которого будешь искать рецепт", reply_markup=markup)



bot.polling(none_stop=True)
