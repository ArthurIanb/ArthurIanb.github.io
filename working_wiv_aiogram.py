from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import os

token = os.environ.get("train_chux_chux_tele_bot")

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    bt = types.KeyboardButton('Open my site', web_app=WebAppInfo(url='https://arthurianb.github.io/'))
    markup.add(bt)
    await message.answer("Hello", reply_markup=markup)

executor.start_polling(dp)
