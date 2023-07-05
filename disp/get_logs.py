from .dispetcher import dp
from aiogram import types
from pandas import DataFrame
import os

from func import delete_message, write_styling_excel
from clas import User, Log


@dp.message_handler(commands=['get_logs'])
async def get_logs(message: types.Message):
    """выгрузка пользовательских событий"""
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 1)
        return await message.answer(
            "Вы не являетесь админом",
            parse_mode='html'
            )

    JSON = await Log.get()

    df = DataFrame(data=JSON)

    FILENAME = '/tmp/users_logs.xlsx'
    SHETNAME = 'logs'

    write_styling_excel(FILENAME, df, SHETNAME)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
    await Log.add(message['from']['id'], 15)
