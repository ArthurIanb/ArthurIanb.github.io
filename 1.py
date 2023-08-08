from telebot import TeleBot, types
from currency_converter import CurrencyConverter
import os



api_tele = os.environ.get("train_chux_chux_tele_bot")
c = CurrencyConverter()
amount = 0


bot = TeleBot(api_tele)
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Hi, I am currency convertor.")
    convert_command(message)


@bot.message_handler(commands=['convert'])
def convert_command(message):
    bot.send_message(message.chat.id, "Whats amount?")
    bot.register_next_step_handler(message, get_amount)


def get_amount(message):
    global amount
    try:
        amount = int(message.text)
        markup = types.InlineKeyboardMarkup(row_width=2)
        usd_eur = types.InlineKeyboardButton("USD to EUR", callback_data='usdeur')
        eur_usd = types.InlineKeyboardButton("EUR to USD", callback_data="eurusd")
        gbp_usd = types.InlineKeyboardButton("GBP to USD", callback_data='gbpusd')
        gbp_eur = types.InlineKeyboardButton("GBP to EUR", callback_data="gbpeur")
        rub_usd = types.InlineKeyboardButton("RUB to USD", callback_data='rubusd')
        rub_eur = types.InlineKeyboardButton("RUB to EUR", callback_data="rubeur")
        other = types.InlineKeyboardButton("Other", callback_data="other")
        markup.add(usd_eur, eur_usd, gbp_usd, gbp_eur, rub_usd, rub_eur)
        markup.add(other)
        bot.send_message(message.chat.id, "Ok, Choice currencies", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "Sorry, invalid amount")


@bot.callback_query_handler(lambda x: True)
def callback_query_handler(callback):
    ans = 0
    if callback.data == 'usdeur':
        ans = c.convert(amount, 'USD', 'EUR')
    elif callback.data == 'eurusd':
        ans = c.convert(amount, 'EUR', 'USD')
    elif callback.data == 'gbpusd':
        ans = c.convert(amount, 'GBP', 'USD')
    elif callback.data == 'gbpeur':
        ans = c.convert(amount, 'GBP', 'EUR')
    elif callback.data == 'rubusd':
        ans = c.convert(amount, 'RUB', 'USD')
    elif callback.data == 'rubeur':
        ans = c.convert(amount, 'RUB', 'EUR')
    elif callback.data == 'other':
        bot.send_message(callback.message.chat.id, "Whats source?")
        bot.register_next_step_handler(callback.message, get_source_curr)
        return
    bot.send_message(callback.message.chat.id, f'Its {ans}')


def get_source_curr(message):
    source_curr = message.text
    bot.send_message(message.chat.id, "Cool")
    bot.send_message(message.chat.id, "Whats the currency your converting to?")
    bot.register_next_step_handler(message, get_currency, source_curr)


def get_currency(message, source_curr):
    currency = message.text
    try:
        res = c.convert(amount, source_curr, currency)
        bot.send_message(message.chat.id, f"The result {res}")
    except:
        bot.send_message(message.chat.id, "Fail")


bot.polling(non_stop=True)
