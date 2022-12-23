import time
from datetime import datetime
import random
import pandas
import telebot
from telebot import types

import rest_and_partn
from db import Database
from send import SendAdmin
from rest_and_partn import Restaurants

import programs
token = 'Тут нужно ввести токен'
bot = telebot.TeleBot(token)

db = Database('database.db')
send = SendAdmin()
restorants = Restaurants(pandas.read_excel('restorans.xlsx', sheet_name='rest'))
musics = rest_and_partn.groups()

programs_10_day = programs.Schedule(pandas.read_excel('programs.xlsx', sheet_name='10'))
programs_11_day = programs.Schedule(pandas.read_excel('programs.xlsx', sheet_name='11'))

menu = ['Где ЕСТЬ?', 'Что поЕСТЬ?', 'Программа', 'Сайт', 'Фото', 'Oрганизаторы и партнеры', 'Вспомнить прошлый ЕСТЬ!']
key_1_where = types.KeyboardButton(menu[0])
key_2_rest = types.KeyboardButton(menu[1])
key_3_programs = types.KeyboardButton(menu[2])
key_4_site = types.KeyboardButton(menu[3])
key_5_photos = types.KeyboardButton(menu[4])
key_6_org = types.KeyboardButton(menu[5])
key_7_org = types.KeyboardButton(menu[6])

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add(key_1_where, key_2_rest, key_3_programs, key_4_site, key_5_photos, key_6_org, key_7_org)

text_insta = '\n<i>В ссылках возможно упоминание Инстаграм и Фейсбук. Деятельность компании Meta Platforms Inc., ' \
             'которой принадлежит ' \
             'Инстаграм / Фейсбук, запрещена на территории РФ в части реализации данных социальных сетей на основании ' \
             'осуществления ею экстремистской деятельности. \n' \
             'Ссылки предоставляют участники фестиваля ЕСТЬ!</i> '

choice_menu = [['Ща всё сделаем.', 'Не переживай, всё будет круть!'],
               ['Кладём бумажонки с надписями ресторанов в шляпу...', 'Мешаем - мешаем - мешаем... \n Достаём...'],
               ['Опять в эти ваши игрульки играете? Ну ладно...', 'Ведётся поиск в базе данных'],
               ['Инициирую поиск твоего ресторана...', 'Где-же он...'],
               ['Эй, зачем разбудили...', 'Сейчас - сейчас выберу вам ресторан, не переживайте'],
               ['Сканирую...', 'Ведётся выбор...'],
               ['Вижу восход прекрасной луны...', 'Вижу, грядут вкусности...'],
               ['Шапочка выбирает ресторан...', 'Но она не волшебная, а простая, как горох'],
               ['Если тебе станет грустно, я букву Г заменю на Х...', 'И теперь ты не Грустишь, а Хрустишь\n чем-то '
                                                                     'вкусненьким из ресторана...'],
               ['Вика, фестиваль начался! Шабашь посты!', 'Ой, да, выбираем ресторан уже...'],
               ['All You Need Is <s>Love</s> плов', 'А может быть и плов, сейчас узнаем.'],
               ]

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            try:
                db.add_user(message.from_user.id)
            except:
                pass

        mess = f'Привет, <b>{message.from_user.first_name}  {message.from_user.last_name}!</b>\nДобро пожаловать на ' \
               f'фестиваль ЕСТЬ! — самый большой гастрономический фестиваль в Поволжье.\n' \
               f'<b>Место</b>:\t Уфа, парковка ТДК "Гостиный двор."\n' \
               f'<b>Дата</b>:\t 10 и 11 сентября.\n'
        bot.send_message(message.chat.id, mess, parse_mode='html')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


# @bot.message_handler(content_types=['photo'])
# # админ присылает фото для рассылки, функ добавляет его в словарь
# def admin_send_photo(message):
#     if message.chat.type == 'private':
#         if message.from_user.id == 1020629:
#             photo = max(message.photo, key=lambda x: x.height)
#             send.get_img(photo.file_id)
#             print(photo.file_id)
#             print(message.content_types)

@bot.message_handler(content_types=['video'])
# админ присылает фото для рассылки, функ добавляет его в словарь
def admin_send_photo(message):
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:
            video = message.video
            send.get_img(video.file_id)
            print(video.file_id)


@bot.message_handler(commands=['adminsendlink'])
# админ присылает ссылку для рассылки, функ добавляет его в словарь
def admin_send_link(message):
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:
            link = message.text
            send.get_link(link)
            print(send)


@bot.message_handler(commands=['adminsendtext'])
# админ присылает текст для рассылки, функ добавляет его в словарь
def admin_send_text(message):
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:
            text = message.text
            send.get_text(text)


@bot.message_handler(commands=['adminsendall'])
# фун для рассылки по бд
def send_all_mes(message):
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:  # айди админа
            link = send.res_mes['link'][14:]
            text = send.res_mes['text'][14:]

            users = db.get_users()
            for row in users:

                try:

                    bot.send_video(row[0], video=send.res_mes['photo'])
                    bot.send_message(row[0], text)
                    bot.send_message(row[0], link)

                    if int(row[1]) != 1:
                        db.set_active(row[0],
                                      1)  # если пользователь не был активен, но получил наше сообщение, то меняем ему
                        # статус на активный
                    else:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[1], 0)  # не получил -  меняем на не активный статус
            bot.send_message(message.from_user.id, 'Рассылка прошла')


@bot.message_handler(commands=['help'])
# основное меню без приветствия
def get_away(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def subcategory(message):
    # создается подкатегория и идем по ответам
    if message.text == 'Программа':
        subcategory = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        programs_3_1 = types.KeyboardButton('Афиша с расписанием')
        programs_3_2 = types.KeyboardButton('Группы')
        programs_3_3 = types.KeyboardButton('Мероприятия для детей')
        programs_3_4 = types.KeyboardButton('Мастер-классы от поваров')
        programs_3_5 = types.KeyboardButton('Конкурсы для гостей фестиваля')
        programs_3_6 = types.KeyboardButton('Уфимская кухня')
        away = types.KeyboardButton('Вернуться в основное меню')
        subcategory.add(programs_3_1, programs_3_2, programs_3_3, programs_3_4, programs_3_5, programs_3_6,
                        away)
        bot.send_message(message.chat.id, 'Выберите нужный ответ:', reply_markup=subcategory)

    elif message.text == 'Афиша с расписанием':
        programs1 = telebot.types.InlineKeyboardMarkup()
        programs1.add(telebot.types.InlineKeyboardButton(text='10 сентября', callback_data='prog_1'))
        programs1.add(telebot.types.InlineKeyboardButton(text='11 сентября', callback_data='prog_2'))
        bot.send_message(message.chat.id, text='Афиша \n Выберите дату:', reply_markup=programs1)


    elif message.text == 'Группы':
        text = 'Будем дэнсить!\n' \
               'Выбери группу, чтобы посмотреть подробную инфу:'
        groups1 = telebot.types.InlineKeyboardMarkup()

        for data in rest_and_partn.groups():
            btm_groups = str(data[3])
            groups1.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_groups))

        bot.send_message(message.from_user.id, text,
                         reply_markup=groups1)

    elif message.text == 'Мероприятия для детей':
        programs1 = telebot.types.InlineKeyboardMarkup()
        programs1.add(telebot.types.InlineKeyboardButton(text='10 сентября', callback_data='child_1'))
        programs1.add(telebot.types.InlineKeyboardButton(text='11 сентября', callback_data='child_2'))
        bot.send_message(message.chat.id, text='Выберите дату:', reply_markup=programs1)


    elif message.text == 'Мастер-классы от поваров':
        bot.send_message(message.chat.id, 'Как только появится инфа, мы её добавим и расскажем об этом ;)')

    elif message.text == 'Конкурсы для гостей фестиваля':
        programs1 = telebot.types.InlineKeyboardMarkup()
        programs1.add(telebot.types.InlineKeyboardButton(text='10 сентября', callback_data='contest_1'))
        programs1.add(telebot.types.InlineKeyboardButton(text='11 сентября', callback_data='contest_2'))
        bot.send_message(message.chat.id, text='Выберите дату:', reply_markup=programs1)

    elif message.text == 'Уфимская кухня':

        programs1 = telebot.types.InlineKeyboardMarkup()
        programs1.add(telebot.types.InlineKeyboardButton(text='10 сентября', callback_data='ufa_1'))
        programs1.add(telebot.types.InlineKeyboardButton(text='11 сентября', callback_data='ufa_2'))
        bot.send_message(message.chat.id, text='Выберите дату:', reply_markup=programs1)




    elif message.text == 'Вернуться в основное меню':
        get_away(message)

    if message.text == 'Что поЕСТЬ?':
        subcategory_rest = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        rest_2_1 = 'Выбрать ресторан'
        rest_2_2 = 'Не знаю, что хочу. Решите за меня!'
        away = types.KeyboardButton('Вернуться в основное меню')
        subcategory_rest.add(rest_2_1, rest_2_2, away)
        bot.send_message(message.chat.id, 'Выберите нужный ответ:', reply_markup=subcategory_rest)

    elif message.text == 'Выбрать ресторан':

        menu1 = telebot.types.InlineKeyboardMarkup()
        menu1.add(telebot.types.InlineKeyboardButton(text='Башкирская кухня', callback_data='btm_1'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Грузинская кухня / Плов', callback_data='btm_2'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Итальянская кухня / Пицца / Паста', callback_data='btm_4'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Мясо: брискет, стейки и так далее)', callback_data='btm_3'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Бургеры / Стрит-фуд', callback_data='btm_5'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Морепродукты / Устрицы / Креветки', callback_data='btm_6'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Паназия / Японская кухня', callback_data='btm_7'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Турецкая / Немецкая кухня', callback_data='btm_12'))
        menu1.add(
            telebot.types.InlineKeyboardButton(text='Выпечка / Круассаны / Десерты / Мороженое', callback_data='btm_8'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Вафли', callback_data='btm_9'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Кофе / Чай ', callback_data='btm_10'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Вино, Пиво и 18+', callback_data='btm_13'))

        bot.send_message(message.chat.id, text='Выберите из списка нижа, чего больше всего хочется', reply_markup=menu1)

    elif message.text == 'Не знаю, что хочу. Решите за меня!':
        random_text = random.choice(choice_menu)

        mes = f'<i>{random_text[0]}</i>'
        bot.send_message(message.chat.id, mes, parse_mode='html')
        time.sleep(1)
        mes = f'<i>{random_text[1]}</i>'
        bot.send_message(message.chat.id, mes, parse_mode='html')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Случайный выбор пал на: ')


        choice_1 = rest_and_partn.rest.random_rest()
        name = choice_1[0]
        value = choice_1[1]
        home = './home/'+ str(choice_1[2]) + '.png'
        img = open(home, 'rb')
        site = choice_1[3]

        markup = types.InlineKeyboardMarkup()
        mes = f'<b>{name}</b>\n{value}\n'
        markup.add(types.InlineKeyboardButton('Перейти на сайт участника', url=site, row_width=1))
        bot.send_message(message.chat.id, mes, reply_markup=markup, parse_mode='html')
        bot.send_photo(message.chat.id, photo=img)

    # раздел воспоминаний
    if message.text == 'Вспомнить прошлый ЕСТЬ!':
        subcategory_rest = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        rest_2_1 = 'Посмотреть видео прошлых лет'
        rest_2_2 = 'Посмотреть фото прошлых лет'
        away = types.KeyboardButton('Вернуться в основное меню')
        subcategory_rest.add(rest_2_1, rest_2_2, away)
        bot.send_message(message.chat.id, 'Выберите нужный ответ:', reply_markup=subcategory_rest)

    elif message.text == 'Посмотреть видео прошлых лет':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Посмотреть все видео', url='https://vk.com/video/@restfestufa'))
        bot.send_message(message.chat.id, 'Нажми на кнопку ниже, чтобы посмотреть все видео с фестиваля ЕСТЬ!',
                         reply_markup=markup)
        video = open('video_1.mp4', 'rb')
        bot.send_video(message.chat.id, video)

    elif message.text == 'Посмотреть фото прошлых лет':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Посмотреть альбомы', url='https://vk.com/albums-169294102'))
        bot.send_message(message.chat.id, 'Нажми на кнопку ниже, чтобы посмотреть фото с фестиваля ЕСТЬ!',
                         reply_markup=markup)

    # смотрим остальные ответы
    if message.text == 'Где ЕСТЬ?':
        latitude = 54.726263
        longitude = 55.944684
        bot.send_location(message.chat.id, latitude, longitude)
        bot.send_message(message.chat.id, 'г.Уфа, парковка ТДК "Гостиный двор"\nРекомендуем оставлять машины за '
                                          'несколько кварталов, чтобы избежать пробок. А лучше приходите без машины '
                                          ';)')
    elif message.text == 'Сайт':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://restfestufa.ru/'))
        bot.send_message(message.chat.id, 'Нажми на кнопку ниже, чтобы перейти на сайт ЕСТЬ!', reply_markup=markup)

    elif message.text == 'Фото':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Посмотреть альбомы', url='https://vk.com/albums-169294102'))
        bot.send_message(message.chat.id, 'Нажми на кнопку ниже, чтобы посмотреть фото с фестиваля ЕСТЬ!',
                         reply_markup=markup)

    elif message.text == 'Oрганизаторы и партнеры':
        bot.send_message(message.chat.id, 'Без них бы не было фестиваля. Спасибо!')

        subcategory_rest = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        part_2_1 = 'Партнеры'
        part_2_2 = 'Информационные партнеры'
        away = types.KeyboardButton('Вернуться в основное меню')
        subcategory_rest.add(part_2_1, part_2_2, away)
        bot.send_message(message.chat.id, 'Выберите нужный ответ:', reply_markup=subcategory_rest)

    if message.text == 'Партнеры':
        partners = rest_and_partn.partners
        part1 = telebot.types.InlineKeyboardMarkup()
        for info in sorted(rest_and_partn.sotred_partners(partners)):
            mes = info[0]
            site = info[2]
            part1.add(telebot.types.InlineKeyboardButton(text=str(mes), url=site))
        bot.send_message(message.chat.id, text='Спасибо нашим партнерам.\nНажмите на кнопку для перехода на сайт:',
                         reply_markup=part1)

    elif message.text == 'Информационные партнеры':

        partners = rest_and_partn.info_partners
        part1 = telebot.types.InlineKeyboardMarkup()
        for info in sorted(rest_and_partn.sotred_partners(partners)):
            mes = info[0]
            site = info[2]
            part1.add(telebot.types.InlineKeyboardButton(text=str(mes), url=site))
        bot.send_message(message.chat.id, text='Спасибо нашим партнерам. \nНажмите на кнопку для перехода на сайт:',
                         reply_markup=part1)


@bot.callback_query_handler(func=lambda call: call.data.startswith('prog'))
def step_rest(call):
    if call.data == 'prog_1':
        mes = '<b>Афиша на 10 сентября</b>'
        bot.send_message(call.from_user.id, mes, parse_mode='html')

        res_mes = ''
        for data in programs_10_day.programs_data:
            time = datetime.strptime(str(data['time']), "%H:%M:%S")
            time = time.strftime('%H:%M')
            name = data['name']
            info = data['info']

            mes = f'<b>{time}</b> — {name}.\n' \
                  f'<i>{info}</i>\n'
            res_mes += mes
        bot.send_message(call.from_user.id, res_mes, parse_mode='html')

    elif call.data == 'prog_2':
        mes = '<b>Афиша на 11 сентября</b>'
        bot.send_message(call.from_user.id, mes, parse_mode='html')

        res_mes = ''
        for data in programs_11_day.programs_data:
            time = datetime.strptime(str(data['time']), "%H:%M:%S")
            time = time.strftime('%H:%M')
            name = data['name']
            info = data['info']

            mes = f'<b>{time}</b> — {name}.\n' \
                  f'<i>{info}</i>\n' \
                  f'\n'
            res_mes += mes
        bot.send_message(call.from_user.id, res_mes, parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('chi'))
def step_rest(call):
    if call.data == 'child_1':
        mes = '<b>Афиша на 10 сентября для детей:</b>'
        bot.send_message(call.from_user.id, mes, parse_mode='html')

        res_mes = ''
        for data in programs_10_day.search_info('дети'):
            t = datetime.strptime(str(data[0]), "%H:%M:%S")
            time = t.strftime('%H:%M')
            name = data[1]
            info = data[2]
            mes = f'<b>{time}</b>\t—\t{name}.\n' \
                  f'<i>{info}</i>\n' \
                  f'\n'

            res_mes += mes
        bot.send_message(call.from_user.id, res_mes, parse_mode='html')

    elif call.data == 'child_2':
        mes = '<b>Афиша на 11 сентября для детей:</b>'
        bot.send_message(call.from_user.id, mes, parse_mode='html')

        res_mes = ''
        for data in programs_11_day.search_info('дети'):
            t = datetime.strptime(str(data[0]), "%H:%M:%S")
            time = t.strftime('%H:%M')
            name = data[1]
            info = data[2]
            mes = f'<b>{time}</b>\t—\t{name}.\n' \
                  f'<i>{info}</i>\n' \
                  f'\n'

            res_mes += mes
        bot.send_message(call.from_user.id, res_mes, parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('ufa'))
def step_rest(call):
    if call.data == 'ufa_1':
        mes = '<b>Ужин с шеф-поваром обладателем звезды Michelin Евгением Викентьевым</b>\n' \
              '\n' \
              'Евгений— яркий представитель современной русской кухни и создатель собственного стиля «intelligent ' \
              'modern cuisine». Действующий шеф-повар ресторана российских деликатесов «Белуга», ex шеф-повар ' \
              'ресторанов «Винный Шкаф», «Hamlet + Jacks» в Санкт-Петербурге, ресторана «Cell» в Берлине. Идеолог ' \
              'современной российской гастрономии, в основу которой вкладывает традиционные локальные продукты, ' \
              'новаторские техники приготовления и нетривиальные сочетания, а целью — получение эмоций от каждого ' \
              'блюда. \n' \
              '\n' \
              'В меню:\n' \
              '• Балтийский угорь, томатный соус, саликорния\n' \
              '• Малиновый тарт, томат, мороженое из икры горбуши\n' \
              '• Мурманская скумбрия, фисташковый соус, кинза\n' \
              '• Пельмени из волжской щуки и фуагра, бульон из сена и грибов, цитрусовая сметана\n' \
              '• Мурманский осьминог, кефир из кокосового молока, баклажан\n' \
              '• Ставропольский барашек, соус из кофе, сельдерей\n' \
              '• Сныть, ганаш из сметаны, ревень\n' \
              '\n' \
              '<i>*ко многим блюдам Евгений подобрал винное сопровождение.</i>\n' \
              '\n' \
              '<b>Сбор гостей в 17:00</b>'

        bot.send_message(call.from_user.id, mes, parse_mode='html')
        logo_file = open('photo10.jpg', 'rb')
        bot.send_photo(call.from_user.id, logo_file)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Заказать билет', url='https://mechti.timepad.ru/event/2150503/'))
        bot.send_message(call.from_user.id, 'Заказать билет и посмотреть подробную информацию:', reply_markup=markup)

    elif call.data == 'ufa_2':
        mes = '<b>11 сентября:</b>\n' \
              '\n' \
              'На протяжении 8 лет обьединение уфимских шеф-поваров "Уфимская Кухня" радует жителей Уфы ' \
              'своими коллаборациями. 2022 год не станет исключением и откроет для города новых гастрономических героев.\n' \
              '\n' \
              'Количество мест ограничено. Вход только по билетам. \n' \
              '\n' \
              '<b>Сбор гостей в 17:00</b>'

        bot.send_message(call.from_user.id, mes, parse_mode='html')
        logo_file = open('photo11.jpg', 'rb')
        bot.send_photo(call.from_user.id, logo_file)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Заказать билет', url='https://mechti.timepad.ru/event/2154770/'))
        bot.send_message(call.from_user.id, 'Заказать билет и посмотреть подробную информацию:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('contest'))
def step_rest(call):
    if call.data == 'contest_1':
        mes = '<b>Конкурсы 10 сентября:</b>'
        bot.send_message(call.from_user.id, mes, parse_mode='html')

        res_mes = ''
        for data in programs_10_day.search_info('конкурс'):
            t = datetime.strptime(str(data[0]), "%H:%M:%S")
            time = t.strftime('%H:%M')
            name = data[1]
            info = data[2]
            mes = f'<b>{time}</b>\t—\t{name}.\n' \
                  f'<i>{info}</i>\n' \
                  f'\n'

            res_mes += mes
        bot.send_message(call.from_user.id, res_mes, parse_mode='html')

    elif call.data == 'contest_2':
        mes = '<b>Конкурсы 11 сентября:</b>'
        bot.send_message(call.from_user.id, mes, parse_mode='html')

        res_mes = ''
        for data in programs_11_day.search_info('конкурс'):
            t = datetime.strptime(str(data[0]), "%H:%M:%S")
            time = t.strftime('%H:%M')
            name = data[1]
            info = data[2]
            mes = f'<b>{time}</b>\t—\t{name}.\n' \
                  f'<i>{info}</i>\n' \
                  f'\n'

            res_mes += mes
        bot.send_message(call.from_user.id, res_mes, parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('btm'))
def step_rest(call):
    text = 'Кликни на название, чтобы узнать подробнее:'
    menu2 = telebot.types.InlineKeyboardMarkup()

    if call.data == 'btm_1':
        rest = rest_and_partn.rest.search_rest('Categories', 'Башкирская кухня')

        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)


    elif call.data == 'btm_2':
        what = ('Плов', 'Грузинская кухня')
        rest = rest_and_partn.rest.search_rest_any('Categories', what)

        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)



    elif call.data == 'btm_3':
        rest = rest_and_partn.rest.search_rest('Categories', 'Мясо')

        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)


    elif call.data == 'btm_4':
        what = ('Пицца', 'Паста')
        rest = rest_and_partn.rest.search_rest_any('Categories', what)
        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)



    elif call.data == 'btm_5':
        what = ('Бургеры', 'Стрит Фуд')
        rest = rest_and_partn.rest.search_rest_any('Categories', what)

        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)

    elif call.data == 'btm_6':
        rest = rest_and_partn.rest.search_rest('Categories', 'Морепродукты')
        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)



    elif call.data == 'btm_7':
        what = ('Японская кухня', 'Паназия')
        rest = rest_and_partn.rest.search_rest_any('Categories', what)
        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)


    elif call.data == 'btm_8':
        rest = rest_and_partn.rest.search_rest('Categories', 'Выпечка')
        for data in rest:
            if len(str(data[2])) <= 4:
                btm_res = str(data[2])
            else:
                btm_res = str(data[4])

            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)


    elif call.data == 'btm_9':
        rest = rest_and_partn.rest.search_rest('Categories', 'Вафли')
        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)


    elif call.data == 'btm_12':
        rest = rest_and_partn.rest.search_rest('Categories', 'Другая')
        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)


    elif call.data == 'btm_10':
        rest = rest_and_partn.rest.search_rest('Categories', 'Кофе')
        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)


    elif call.data == 'btm_13':
        rest = rest_and_partn.rest.search_rest('Categories', 'Напитки')
        for data in rest:
            btm_res = str(data[2])
            menu2.add(telebot.types.InlineKeyboardButton(text=data[0], callback_data=btm_res))

        bot.send_message(call.from_user.id, text,
                         reply_markup=menu2)

    else:
        mes = 'Кажется стейк подгорел. Нужно приготовить его снова...'
        bot.send_message(call.from_user.id, mes, reply_markup=menu2)
        get_away(call)


@bot.callback_query_handler(func=lambda call: len(call.data) <= 4 or len(call.data) > 10)
def step_rest2(call):
    markup = types.InlineKeyboardMarkup()

    mes = ''
    site = ''
    home = ''
    for i in restorants.rest_dict:

        if str(i['id']) == str(call.data):
            name = i['NAME']
            info = i['info']
            site = i['site']

            home = './home/' + str(i['home']) + '.png'

            mes = f'<b>{name}</b>\n' \
                  f'\n{info}\n' \


    markup.add(types.InlineKeyboardButton('Перейти на сайт участника', url=site, row_width=1))
    bot.send_message(call.from_user.id, mes, reply_markup=markup, parse_mode='html')
    img = open(home, 'rb')
    bot.send_photo(call.from_user.id, photo=img)

@bot.callback_query_handler(func=lambda call: call.data.isdigit() and len(call.data) > 4)
def step_rest2(call):
    markup = types.InlineKeyboardMarkup()
    mes = ''
    site = ''
    for i in rest_and_partn.groups():
        if str(i[3]) == call.data:
            name = i[0]
            info = i[1]
            site = i[2]

            mes = f'<b>{name}</b>.\n' \
                  f'\n{info}\n'

    markup.add(types.InlineKeyboardButton('Перейти на сайт', url=site, row_width=1))
    bot.send_message(call.from_user.id, mes, reply_markup=markup, parse_mode='html')


bot.polling(none_stop=True)
