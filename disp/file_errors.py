from .dispetcher import dp
from aiogram import types
import os
from pandas import DataFrame

from func import delete_message, write_styling_excel
from clas import User, ToxicCaseError, Organization


@dp.message_handler(commands=['get_errors'])
async def file_get_errors(message: types.Message):
    await delete_message(message)

    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы неизвестный пользователь!",
            parse_mode='html'
            )
    if USER.role in ['admin', 'rpn']:
        ORG = await Organization.get_org_id_list()
    else:
        ORG = [USER.org]

    JSON = await ToxicCaseError.get_all(ORG)

    df = DataFrame(data=JSON)
    df = df.fillna('')
    if len(df) == 0:
        mess = 'пока не нашел ошибок'
        return await message.answer(mess)
    FILENAME = '/tmp/ошибки заполнения.xlsx'
    SHETNAME = 'def'

    write_styling_excel(FILENAME, df, SHETNAME)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
