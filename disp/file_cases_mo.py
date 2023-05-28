from .dispetcher import dp
from pandas import DataFrame
from aiogram import types
from datetime import datetime
import os

from func import delete_message, return_mounth, \
    write_styling_excel
from clas import User, ToxicCase


@dp.message_handler(commands=['file_cases_mo'])
async def file_cases_mo(message: types.Message):
    await delete_message(message)

    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы неизвестный пользователь!",
            parse_mode='html'
            )

    if USER.role == 'admin':
        MO = 'all'
    else:
        MO = USER.org

    START, END = return_mounth(datetime.now())

    JSON = await ToxicCase.file_cases_mo(START, END, MO)

    df = DataFrame(data=JSON)
    FILENAME = f'/tmp/toxic_case_{str(START)}_{str(END)}.xlsx'
    SHETNAME = 'def'

    write_styling_excel(FILENAME, df, SHETNAME)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
