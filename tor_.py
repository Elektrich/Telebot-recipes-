import requests
from bs4 import BeautifulSoup as bs
import telebot
from telebot import types
import time
import variables as var

# токен бота
TOKEN = "6518544830:AAFYaLYYFUxAU3-KfKtJZtyTRCikr8oRYbQ"
bot = telebot.TeleBot(TOKEN)

def text_of_recipe(req):
    if var.site == "Gastronom":
        r = requests.get(f"https://www.gastronom.ru/search/type/recipe?t={req.text}")
        html = bs(r.text, 'lxml')
        var.work = False
        var.work_second_part = False

        # карточка рецепта
        resipes = html.find_all("article", class_="material-anons col-sm-4 col-ms-6")

        # название всех рецептоа на сайте
        for resp in resipes:
            title_resipe = resp.find("a", class_="material-anons__title")
            if req.text in title_resipe:
                # строчка кода с ссылкой на выбранный рецепт
                kod = str(title_resipe)
                kod_2 = kod.split('"')
                # ищем ссылку среди кода
                for z in kod_2:
                    print(z)
                    if "/" in z and not "/a" in z:

                        # переходим по этой ссылке
                        request = requests.get(f"https://www.gastronom.ru{z}")
                        soup = bs(request.text, "lxml")

                        # ищем ингредиенты для рецепта
                        ingredients = soup.find_all("li", class_="recipe__ingredient")
                        ingredients_text = "ИНГРЕДИЕНТЫ:"
                        # добавляем ингредиенты в строку
                        for i in ingredients:
                            ingredients_text += f'\n{i.text}'
                        # отправлям ингредиенты
                        bot.send_message(req.chat.id, ingredients_text)

                        # ищем шаги приготовления данного рецепта
                        recipe = soup.find_all("div", class_="recipe__step")
                        step = 0
                        for res in recipe:
                            step += 1
                            step_text = f"Шаг {step}"
                            bot.send_message(req.chat.id, f"{step_text:*^20}")

                            # ищем изображения к рецепту
                            img_res = res.find("img", class_="recipe__step-img")

                            # если они есть, то
                            if img_res is not None:

                                # ищем отдельную ссылку на картинку
                                img_split = str(img_res)
                                ssilka = img_split.split('"')
                                for i in ssilka:
                                    if "/" in i:
                                        URL = 'https://api.telegram.org/bot'
                                        img_url = f"https://www.gastronom.ru/{i}"
                                        # отправляем картинку
                                        requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={req.chat.id}&photo={img_url}')

                            # ищем текст к шагу
                            text = res.find("div", class_="recipe__step-text")
                            # отправляем его
                            bot.send_message(req.chat.id, text.text)
                            # жлем полторы секунды, чтобы не спамить
                            time.sleep(1.5)

            elif req.text not in title_resipe.text:
                bot.send_message(req.chat.id, "Не нашел твой рецепт")
                break
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Да", callback_data="yes")
            button2 = types.InlineKeyboardButton("Нет", callback_data="no")
            markup.add(button1, button2)
            bot.send_message(req.chat.id, "Хочешь найти что-нибудь еще?", reply_markup=markup)
            break

    elif var.site == "Art-Lunch":
        r = requests.get(f"https://art-lunch.ru/?s={req.text}")
        html = bs(r.text, 'lxml')
        var.work = False
        var.work_second_part = False

        # карточка рецепта
        resipes = html.find_all("div", class_="col-sm-6 col-md-4 recipe-col mb-3")

        # название всех рецептоа на сайте
        for resp in resipes:
                title_resipe = resp.find("div", class_="card-body")
                if req.text in resp.text:
                    kod = resp.find("a", class_="recipe-link")
                    kod_2 = str(kod)
                    kod_3 = kod_2.split('"')
                    # ищем ссылку среди кода
                    for z in kod_3:
                        if "/recipe/" in z:
                            # переходим по этой ссылке
                            request = requests.get(f"{z}")
                            soup = bs(request.text, "lxml")

                            # ищем ингредиенты для рецепта
                            ing = soup.find("ul", class_="list-unstyled")
                            list_ing = ing.find_all("li")
                            ingredients_text = "ИНГРЕДИЕНТЫ:"
                            for i in list_ing:
                                ingredients = i.find("span", itemprop="recipeIngredient")
                                # добавляем ингредиенты в строку
                                ingredients_text += f'\n{ingredients.text}'
                            # отправлям ингредиенты
                            bot.send_message(req.chat.id, ingredients_text)

                            # ищем шаги приготовления данного рецепта
                            recipe = soup.find("div", itemprop="recipeInstructions")
                            steps = recipe.find_all("p")
                            step = 0
                            for res in steps:
                                step += 1
                                step_text = f"Шаг {step}"
                                bot.send_message(req.chat.id, f"{step_text:*^20}")

                                # ищем изображения к рецепту
                                img_res = res.find("img")

                                # если они есть, то
                                if img_res is not None:
                                    # ищем отдельную ссылку на картинку
                                    img_split = str(img_res)
                                    ssilka = img_split.split('"')
                                    for i in ssilka:
                                        if "https://art-lunch.ru/content/uploads" and ".jpg" and not "300x188" in i:
                                            URL = 'https://api.telegram.org/bot'
                                            img_url = f"{i}"
                                            # отправляем картинку
                                            requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={req.chat.id}&photo={img_url}')

                                # ищем текст к шагу
                                # отправляем его
                                bot.send_message(req.chat.id, res.text)

                elif req.text not in title_resipe.text:
                    bot.send_message(req.chat.id, "Не нашел твой рецепт")
                    break
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton("Да", callback_data="yes")
                button2 = types.InlineKeyboardButton("Нет", callback_data="no")
                markup.add(button1, button2)
                bot.send_message(req.chat.id, "Хочешь найти что-нибудь еще?", reply_markup=markup)
                break
