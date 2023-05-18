"""
Этот бот написан для всяких мелких задач с регизом
Автор Медовиков Олег
2022
""" 

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import BoundFilter
    
from conf import TELEGRAM_TOKEN
from func import *
from clas import User
from base import database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp  = Dispatcher(bot)

async def on_startup(dp):
    await database.connect()
    await set_default_commands(dp)
    
class IsKnown(BoundFilter):
    key = 'is_know'
    
    def __init__(self, is_know):
        self.is_know = is_know

    async def check(self, message: types.Message):
        USER = User(
            u_id= message['from']['id'],
            first_name= message['from']['first_name'],
            last_name= message['from']['last_name'],
            username= message['from']['username']
                    )
        res = await USER.check()
        if not res:
            await USER.add_people() 
            await message.answer('Только для известных пользователей')
        return res 

dp.filters_factory.bind(IsKnown)

@dp.message_handler(is_know=True, commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(hello_message(message['from']), parse_mode='html')

@dp.message_handler(is_know=True, commands=['meddoc'])
async def send_meddoc_by_id(message : types.Message):
    arg = str(message.get_args())
    if arg == '':
        await message.reply('Добавьте к команде номер документа для поиска')
    else:
        try:
            MEDDOC_ID = int(arg)
        except AttributeError:
            await message.reply('Номер документа должен быть числом')
        else:
            res = meddoc_by_case(MEDDOC_ID)
            await message.answer(res)

if __name__ == '__main__':
    executor.start_polling(
            dp,
            skip_updates=True, 
            on_startup=on_startup)

