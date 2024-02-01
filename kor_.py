import requests
from bs4 import BeautifulSoup as bs
import telebot
from telebot import types
import variables as var

# токен бота
TOKEN = "6518544830:AAFYaLYYFUxAU3-KfKtJZtyTRCikr8oRYbQ"
bot = telebot.TeleBot(TOKEN)

def katalog_of_resipes(message):
    if var.site == "Gastronom":

        r = requests.get(f"https://www.gastronom.ru/search/type/recipe?t={message.text}")
        html = bs(r.text, 'lxml')

        resipes = html.find_all("article", class_="material-anons col-sm-4 col-ms-6")
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Да", callback_data="yea")
        button2 = types.InlineKeyboardButton("Нет", callback_data="not")
        markup.add(button1, button2)

        res_s = []
        for resp in resipes:
            title_resp = resp.find("a", class_="material-anons__title")
            res_s.append(title_resp.text)

        if len(res_s) == 0:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Да", callback_data="not")
            button2 = types.InlineKeyboardButton("Нет", callback_data="no")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Не нашел рецепты по твоему запросу. Перезапустить?", reply_markup=markup)

        else:
            print(len(res_s))
            bot.send_message(message.chat.id, "Вот все рецепты, которые я смог найти:")
            for res in res_s:
                bot.send_message(message.chat.id, res)

            bot.send_message(message.chat.id, "Нашел нужный тебе рецепт?", reply_markup=markup)

    elif var.site == "Art-Lunch":

        r = requests.get(f"https://art-lunch.ru/?s={message.text}")
        html = bs(r.text, 'lxml')

        resipes = html.find_all("div", class_="col-sm-6 col-md-4 recipe-col mb-3")
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Да", callback_data="yea")
        button2 = types.InlineKeyboardButton("Нет", callback_data="not")
        markup.add(button1, button2)

        res_s = []
        for resp in resipes:
            title_resp = resp.find("div", class_="card-body")
            res_s.append(title_resp.text)

        if len(res_s) == 0:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Да", callback_data="not")
            button2 = types.InlineKeyboardButton("Нет", callback_data="no")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Не нашел рецепты по твоему запросу. Перезапустить?", reply_markup=markup)

        else:
            print(len(res_s))
            bot.send_message(message.chat.id, "Вот все рецепты, которые я смог найти:")
            for res in res_s:
                bot.send_message(message.chat.id, res)

            bot.send_message(message.chat.id, "Нашел нужный тебе рецепт?", reply_markup=markup)


