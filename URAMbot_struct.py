import requests
import telebot
from telebot import types
token = '5076012878:AAFqm5lP8WC5qBpN_HfsCnYkr2l81DNIfJc'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('История поездок')
    item2 = types.KeyboardButton('Ближайший самокат')
    item3 = types.KeyboardButton('Информация')
    markup.add(item1, item2, item3)
    bot.send_message(m.chat.id, 'Приветствую тебя, {0.first_name}!, я информационный бот. '
                                '\n Для получения информации можете воспользоваться подсказками ниже'.format(m.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def phone(m, res=False):
    if m.chat.type == 'private':
        if m.text == 'История поездок':

            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text='Узнать историю поездки', request_contact=True)
            markup.add(button_phone)
            bot.send_message(m.chat.id, 'Поделитесь контактом чтоб посмотреть свою историю поездки', reply_markup=markup)
        elif m.text == 'Ближайший самокат':
            pass
        elif m.text == 'Информация':
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            item1 = types.KeyboardButton(text='Оплата')
            item2 = types.KeyboardButton(text='Как поехать')
            item3 = types.KeyboardButton(text='Как закончить')
            item4 = types.KeyboardButton(text='Как найти')
            keyboard.add(item1, item2, item3, item4)
            bot.send_message(m.chat.id, 'Какая информация вас интересует?', reply_markup=keyboard)
        elif m.text == 'Оплата':
            bot.send_message(m.chat.id, "Оплатить можно по карте."
                                        "\nСтоимость: 1мин. = 5руб."
                                        "\n Ожидание: 0,5руб.")
        elif m.text == 'Как поехать':
            bot.send_message(m.chat.id, 'Чтобы включить электросамокат, достаточно найти его в приложении.'
                                        'Она расположена на руле рядом с информативным дисплеем.'
                                        '\nКогда самокат включится, нажмите специальный курок на руле'
                                        ' самоката и он поедет. Курок расположен на правой рукоятке.')
        elif m.text == 'Как закончить':
            bot.send_message(m.chat.id, "Нужно оставить самокат и заблокировать его.")
        elif m.text == 'Как найти':
            bot.send_message(m.chat.id, "Найти его можно по карте. Или на парковке.")




        elif m.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            item1 = types.KeyboardButton('История поездок')
            item2 = types.KeyboardButton('Ближайший самокат')
            item3 = types.KeyboardButton('Информация')
            markup.add(item1, item2, item3)
            bot.send_message(m.chat.id, 'Назад', reply_markup = markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Оплата':
        bot.send_message(message.from_user.id, 'Оплатить можно по карте. \n Стоимость: 1мин. = 5руб.'
                                            ' \n Ожидание: 0,5руб."')
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши привет.')
    elif message.text == 'Никнейм':
        bot.send_message(message.chat.id, f'Your Nik: {message.from_user.first_name}')
    elif message.text == 'ID':
        bot.send_message(message.from_user.id, f'Your ID: {message.from_user.id}')
    else:
        bot.send_message(message.from_user.id, 'напиши /help.')


#модуль ближайший самокат
@bot.message_handler(content_types='')
def nearest_scoot():
    url = 'https://uram.ddns.net/uram_bot/find'

    req = {'lat': '12', 'lon': '12'}
    data = '56.9993738'
    data2 = '54.953738'
    data3 = '+79195527202'
    req['lat'] = data
    req['lon'] = data2
    req['phone'] = data3
    req_j = requests.post(url, json=req)
    req_data = req_j.json()
    print(req_j.url)
    print(req_j.status_code)
    da = req_j.text
    print(da)
    print(req_data)

t = nearest_scoot()






#Модуль история поездок
@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)
        pol = '+' + message.contact.phone_number
    def history():
        phn = {'phone': pol}
        url = 'https://uram.ddns.net/uram_bot/history'
        req_j = requests.post(url, json=phn)
        req_data = req_j.json()
        if req_j.status_code == 200:
            try:
                for req_data['history'][0] in req_data['history']:
                    bot.send_message(message.from_user.id, 'Цена: ' + str(req_data['history'][0]['cost']) +
                    '\nНачало: ' + req_data['history'][0]['start_time'] +
                    '\nКонец: ' + req_data['history'][0]['end_time'] +
                    '\nСтатус поездки: ' + req_data['history'][0]['status'])
                    req_data['history'][+1]
            except KeyError:
                print('Что то пошло не так')
            except IndexError:
                print()
        else:
            print('Что то пошло не так')
    t = history()











print('bot started')
bot.polling(none_stop=True, interval=0)
