import telebot
from bs4 import BeautifulSoup
import requests
from random import randint


token = ''
bot = telebot.TeleBot(token)
url_rf = 'https://index.minfin.com.ua/reference/coronavirus/geography/russia/'


@bot.message_handler(commands=['start'])
def first_message(message):
    """Greeting and keyboard output."""
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Статистика по миру', 'Статистика по России')
    keyboard.row('Заражён ли я?')
    bot.send_message(message.chat.id, 'Привет, что хочешь узнать?',
                     reply_markup=keyboard)


@bot.message_handler(regexp='Статистика по России')
def stats_rf(message):
    """ It displays statistics on coronavirus from the website of
        the Ministry of Finance, but for Russia.
    """
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
    """ Displays statistics on coronavirus from the website of
        the Ministry of Finance.
    """
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
    """With a 50 to 50 chance, it shows your result on coronavirus."""
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
    """Re-conducting a coronavirus test."""
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


@bot.message_handler(commands=['info'])
def what(message):
    """Information about the bot."""
    bot.send_message(message.chat.id, '🤑My bitcoin wallet🤑\
                                       1FLApcQPyJVmf3uevcN2JiXWpWD86xEVod')


@bot.message_handler(content_types=['text'])
def wrong_command(message):
    """Unknown message."""
    bot.send_message(message.chat.id, '???????????????????')


if __name__ == '__main__':
    bot.infinity_polling()
