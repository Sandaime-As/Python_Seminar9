from random import randint, choice
from telebot import types
import telebot
token = "5886409205:AAEZoUoEFyFEWq7vy5gNJx0XWWNltxvUMM8"
bot = telebot.TeleBot(token)
table = dict()
turn = dict()
game = dict()
game_mode = dict()
order = dict()


def check_win(message):
    global game, order
    if table[message.chat.id] <= 28:
        if game_mode[message.chat.id] == 'Игрок против Игрока':
            bot.send_message(
                message.chat.id, f'Победил игрок № {1 if turn else 2}')
            game[message.chat.id] = False
        if game_mode[message.chat.id] == 'Игрок против Бота':
            bot.send_message(
                message.chat.id, f"Победитель {'Игрок' if order[message.chat.id]==1 else 'Бот'}")
            game[message.chat.id] = False


def new_game(message):
    global game, table, turn
    game[message.chat.id] = True
    table[message.chat.id] = 127
    turn[message.chat.id] = choice([True, False])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую Вас!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Новая игра')
    item2 = types.KeyboardButton('Игра против Игрока')
    item3 = types.KeyboardButton('Игра против Бота')
    markup.add(item2, item3)
    markup.add(item1)

    bot.send_message(message.chat.id, 'Начнем игру',
                     reply_markup=markup)


def handle_game_proc(message):
    global game
    try:
        if game[message.chat.id] and 1 <= int(message.text) <= 28:
            print('100')
            return True
        else:
            print('101')
            return False
    except KeyError:
        game[message.chat.id] = False
        if game[message.chat.id] and 1 <= int(message.text) <= 28:
            print('102')
            return True
        else:
            print('103')
            return False


@bot.message_handler(content_types='text')
def message_reply(message):
    global game_mode
    if message.text == 'Новая игра':
        new_game(message)
        bot.send_message(
            message.chat.id, 'Начнем новую игру')

    if message.text == 'Игра против игрока':
        new_game(message)
        game_mode[message.chat.id] = 'Игрок против Игрока'
        bot.send_message(
            message.chat.id, f'Тянет игрок номер {1 if turn[message.chat.id] else 2}')

    if message.text == 'Игра против бота':
        new_game(message)
        game_mode[message.chat.id] = 'Игрок против Бота'
        bot.send_message(
            message.chat.id, f"Тянет {'Игрок' if turn[message.chat.id] else 'Бот'}")
        if not (turn[message.chat.id]):
            hand = randint(1, 29)
            table[message.chat.id] -= hand
            bot.send_message(
                message.chat.id, f'Бот взял {hand}')
            bot.send_message(
                message.chat.id, f'На столе осталось {table[message.chat.id]} конфет')
            bot.send_message(
                message.chat.id, f'Тянет игрок')
            check_win(message)
            turn[message.chat.id] = not (turn[message.chat.id])

    else:
        game_run(message)


def game_run(message):
    global game, table, turn, game_mode, order
    check_win(message)
    if 1 <= int(message.text) <= 28 and game[message.chat.id]:

        if game_mode[message.chat.id] == 'Игрок проив игрока' and game_mode[message.chat.id]:

            table[message.chat.id] -= int(message.text)
            bot.send_message(
                message.chat.id, f"На столе осталось {table[message.chat.id]} конфет")
            turn[message.chat.id] = not (turn[message.chat.id])
            bot.send_message(
                message.chat.id, f"Теперь тянет игрок №{1 if turn[message.chat.id] else 2} ")

        if game_mode[message.chat.id] == 'Игра против Бота' and game_mode[message.chat.id]:

            if turn[message.chat.id]:
                order[message.chat.id] = 1
                table[message.chat.id] -= int(message.text)
                bot.send_message(
                    message.chat.id, f'Игрок взял {message.text}')
                bot.send_message(
                    message.chat.id, f'На столе осталось {table[message.chat.id]} конфет')

                bot.send_message(
                    message.chat.id, f'Ход Бота')
                if table[message.chat.id] > 28:
                    hand = randint(1, 29)
                    table[message.chat.id] -= hand
                    bot.send_message(
                        message.chat.id, f"Бот забрал {hand}")
                    bot.send_message(
                        message.chat.id, f"На столе осталось {table[message.chat.id]} конфет")
                    bot.send_message(
                        message.chat.id, f"Ход игрока")
                    order[message.chat.id] = 1

    elif game[message.chat.id]:
        bot.send_message(
            message.chat.id, f"Можно вводить только до 28")
    check_win(message)


bot.infinity_polling()
