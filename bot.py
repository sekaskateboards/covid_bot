import telebot
from config import token
from bs4 import BeautifulSoup
import requests
from random import randint


bot = telebot.TeleBot(token)
url_rf = 'https://index.minfin.com.ua/reference/coronavirus/geography/russia/'
# разберись почему ты не можешь из файла конфиг вынести токен сюда
# файловый ввод/вывод используй, но мб нагуглишь более красивый способ


@bot.message_handler(commands=['start'])
def first_message(message):
    """Вывод приветсвия и показ команд."""
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Статистика по миру', 'Статистика по России')
    keyboard.row('Заражён ли я?')
    bot.send_message(message.chat.id, 'Привет, что хочешь узнать?',
                     reply_markup=keyboard)


@bot.message_handler(regexp='Статистика по России')
def stats_rf(message):
    """Выводит статистику по коронавирусу с сайта МинФина, но по России."""
    requ_rf = requests.get(url_rf)
    soup = BeautifulSoup(requ_rf.content, 'html.parser')
    stats_all = soup.find('strong', class_='black').text
    stats_dead = soup.find('strong', class_='red').text
    stats_healthy = soup.find('strong', class_='green').text
    bot.send_message(message.chat.id, '🇷🇺😷Всего заболевших - ' + stats_all)
    bot.send_message(message.chat.id, '🇷🇺💀Смертельные случаи - ' + stats_dead)
    bot.send_message(message.chat.id, '🇷🇺✨Выздоро­вевшие - ' + stats_healthy)


@bot.message_handler(regexp='Статистика по миру')
def stats_global(message):
    """Выводит статистику по коронавирусу с сайта МинФина."""
    requ_gl = requests.get('https://index.minfin.com.ua/reference/coronavirus')
    soup = BeautifulSoup(requ_gl.content, 'html.parser')
    stats_all = soup.find('strong', class_='black').text
    stats_dead = soup.find('strong', class_='red').text
    stats_healthy = soup.find('strong', class_='green').text
    bot.send_message(message.chat.id, '😷Всего заболевших - ' + stats_all)
    bot.send_message(message.chat.id, '💀Смертельные случаи - ' + stats_dead)
    bot.send_message(message.chat.id, '✨Выздоро­вевшие - ' + stats_healthy)


@bot.message_handler(regexp='Заражён ли я?')
def corona_test(message):
    """С шансом 50 на 50 показывает ваш результат на коронавирус."""
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Проверить ещё раз',
                                                  callback_data='yes'))
    rand = randint(0, 11)
    if rand >= 5:
        bot.send_photo(message.chat.id, 'https://clck.ru/MkPER',
                       reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сейчас - нет🦠',
                                          reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    """Заново проводит тест на коронавирус."""
    if call.data == 'yes':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        # Удаляет предыдущий результат на коронавирус
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Проверить ещё раз',
                                                      callback_data='yes'))
        rand = randint(0, 11)
        if rand >= 5:
            bot.send_photo(call.message.chat.id, 'https://clck.ru/MkPER',
                           reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, 'Сейчас - нет🦠',
                             reply_markup=markup)
        # проводит тест на коронавирус


@bot.message_handler(commands=['info'])
def what(message):
    """Информация о боте."""
    bot.send_message(message.chat.id, '🤑My bitcoin wallet🤑\
                                       1FLApcQPyJVmf3uevcN2JiXWpWD86xEVod')


@bot.message_handler(content_types=['text'])
def wrong_command(message):
    """ffff."""
    bot.send_message(message.chat.id, '???????????????????')


if __name__ == '__main__':  # бесконечный цикл по типу while 0 == 0
    bot.infinity_polling()
