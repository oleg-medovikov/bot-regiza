"""
Этот бот написан для всяких мелких задач с регизом
Автор Медовиков Олег
2022
"""

import logging
from aiogram import Bot, Dispatcher, executor, types

from conf import TELEGRAM_TOKEN
from func import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp  = Dispatcher(bot)

async def on_startup(dp):
    await set_default_commands(dp)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user = message['from']
    await message.answer(hello_message(user), parse_mode='html')

@dp.message_handler(commands=['meddoc'])
async def send_meddoc_by_id(message : types.Message):
    arg = message.get_args()
    if arg == '':
        await message.reply('Добавьте к команде номер документа для поиска')
    else:
        try:
            MEDDOC_ID = int(arg)
        except:
            await message.reply('Номер документа должен быть числом')
        else:
            res = meddoc_by_case(MEDDOC_ID)
            await message.answer(res)

if __name__ == '__main__':
    executor.start_polling(
            dp,
            skip_updates=True, 
            on_startup=on_startup)



