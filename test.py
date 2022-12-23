# @bot.message_handler(commands=['start', 'help'])
# def category(message):
#     keyboard_category = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     key_1_1 = types.KeyboardButton('Где ЕСТЬ?')
#     keyboard_category.add(key_1_1)
#
#     bot.reply_to(message, "Привет! Я помогу подобрать товар!", reply_markup=keyboard_category)
#
#
# @bot.message_handler(content_types=['text'])
# def subcategory(message):
#     if message.text == "1_1":
#         keyboard_subcategory = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         key_2_1 = types.KeyboardButton('2_1')
#         keyboard_subcategory.add(key_2_1)  # key_2_1 не использовалась
#
#         bot.send_message(message.chat.id, 'Выберите подкатегорию', reply_markup=keyboard_subcategory)
#
#     elif message.text == "2_1":
#         keyboard_tovar = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         key_3_1 = types.KeyboardButton('3_1')
#         keyboard_tovar.add(key_3_1)  # key_3_1 не использовалась
#
#         bot.send_message(message.chat.id, 'Выберите товар по названию и я пришлю вам подробности',
#                          reply_markup=keyboard_tovar)
#
#     elif message.text == "3_1":  # потеряли двоеточие
#         bot.send_message(message.chat.id, "Описание товара")
#         bot.send_photo(message.chat.id, 'https://cs13.pikabu.ru/images/big_size_comm/2020-06_3/159194100716237333.jpg')  # просто укажите ссылку на картинку

# res = {'Разжигатели':
#            {'site': 'https://fire.smartomato.ru/menu',
#             'info': 'Тот самый брискет',
#             'home': 'Домик № такой-то'},
#        'Китчен':
#            {'site': 'https://kitplaneta.smartomato.ru/menu',
#             'info': 'Всякое разное',
#             'home': 'Домик № такой-то'},
#        'Дублин':
#            {'site': 'https://dublin.smartomato.ru/menu',
#             'info': 'Ирландский паб',
#             'home': 'Домик № такой-то'},
#        }
#
#
# def sort_rest(dict):
#     site = ''
#     info = ''
#     home = ''
#     for name, value in sorted(dict.items()):
#         for i_k, i_v in value.items():
#             if i_k == 'site':
#                 site = i_v
#             if i_k == 'info':
#                 info = i_v
#             if i_k == 'home':
#                 home = i_v
#         yield name, info, home, site
#
#
# import time
# import random
# import os
# # time.sleep(2)
#
# food_giff = ['1.mp4', '2.mp4', '3.mp4', '4.mp4', '5.mp4', '6.mp4', '7.mp4', '8.mp4', '9.mp4']
#
# random_rest = random.choice(list(res.items()))
# random_giff = random.choice(food_giff)
# path = "C:\\Users\\Nastya\\PycharmProjects\\pythonProject\\Bot\\gif_food\\" + random_giff
# file = open(path)
#
# name = random_rest[0]
# value = random_rest[1]
# site = value['site']
# info = value['info']
# home = value['home']
#
# print(name, info)
# print(info['info'])
# print(info['home'])
# print(info['])
#
# test = {'Id': '1020629', 'User': 'Anastasia'}
#
#
# def check_id_in_file(users_dict, user_id):
#     """проверяет есть ли id пользователя в бд"""
#     for i_id in users_dict.keys():
#         if i_id == user_id:
#             print('Такой id уже есть')
#             return True
#         else:
#             print('Такого id нету')
#             return False
#
#
# print(check_id_in_file(test, '1020629'))


# def file_user_id(id):
#     """записывает данные пользователей: id и первое имя"""
#     file = open('users.txt', 'w+')
#     for line in file:
#         print(line)
#     # if check_id_in_file(dict_f, message.from_user.id) is True:
#     file.write("Id: {}\n".format(id))
#     file.close()


# file_user_id(45644)
# file = open('users.txt', 'w+')
# for line in file:
#     if id in line:
#         print('True')
#     else:
#         file.write(id)
#         print('False')
# file.close()


# id: 8789, user: Kari

import re

# file = {'id': '8789', 'user': 'Kari'}
# reg_exp = fr"'{re.escape(id)}'"
# print(reg_exp)

# with open('users.txt', 'r+', encoding='utf-8') as file:
#     for line in file:
#         print(line)
#         if id not in line:
#             mes = f'\n{id}'
#             file.write(mes)
#             print('N')
#         else:
#             print('Y')
# file.close()
# Id: 1021629, User: Anastasia

# def file_user_id(message):
#     """записывает данные пользователей: id и первое имя"""

# file = open('users.txt', 'r+', encoding='utf-8')
# data = file.readlines()
# print(data)
# search = '1020629' + '\n'
# if search not in data:
#     print('Chirp')
    # if message.from_user.id in data:
    #     print('Y')
    # else:
    #     print('N')
    #     file.write("Id: {}, User: {}\n".format(message.from_user.id, message.from_user.first_name))
    # file.close()

# id_file = open('users.txt', 'r')
# for user_id in id_file.readlines():
#     print(user_id)
# from random import *
# from turtle import *
#
# from freegames import floor, vector
#
# tiles = {}
# neighbors = [
#     vector(100, 0),
#     vector(-100, 0),
#     vector(0, 100),
#     vector(0, -100),
# ]
#
#
# def load():
#     """Load tiles and scramble."""
#     count = 1
#
#     for y in range(-200, 200, 100):
#         for x in range(-200, 200, 100):
#             mark = vector(x, y)
#             tiles[mark] = count
#             count += 1
#
#     tiles[mark] = None
#
#     for count in range(1000):
#         neighbor = choice(neighbors)
#         spot = mark + neighbor
#
#         if spot in tiles:
#             number = tiles[spot]
#             tiles[spot] = None
#             tiles[mark] = number
#             mark = spot
#
#
# def square(mark, number):
#     """Draw white square with black outline and number."""
#     up()
#     goto(mark.x, mark.y)
#     down()
#
#     color('black', 'white')
#     begin_fill()
#     for count in range(4):
#         forward(99)
#         left(90)
#     end_fill()
#
#     if number is None:
#         return
#     elif number < 10:
#         forward(20)
#
#     write(number, font=('Arial', 60, 'normal'))
#
#
# def tap(x, y):
#     """Swap tile and empty square."""
#     x = floor(x, 100)
#     y = floor(y, 100)
#     mark = vector(x, y)
#
#     for neighbor in neighbors:
#         spot = mark + neighbor
#
#         if spot in tiles and tiles[spot] is None:
#             number = tiles[mark]
#             tiles[spot] = number
#             square(spot, number)
#             tiles[mark] = None
#             square(mark, None)
#
#
# def draw():
#     """Draw all tiles."""
#     for mark in tiles:
#         square(mark, tiles[mark])
#     update()
#
#
# setup(420, 420, 370, 0)
# hideturtle()
# tracer(False)
# load()
# draw()
# onscreenclick(tap)
# done()