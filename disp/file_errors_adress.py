from .dispetcher import dp
from aiogram import types
import os
from pandas import DataFrame

from func import delete_message, write_styling_excel
from clas import User, Adress, Organization, Log


@dp.message_handler(commands=['get_errors_adress'])
async def file_errors_adress(message: types.Message):
    await delete_message(message)

    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 2)
        return await message.answer(
            "вы неизвестный пользователь!",
            parse_mode='html'
            )
    if USER.role in ['admin', 'rpn']:
        ORG = await Organization.get_org_id_list()
    else:
        ORG = [USER.org]

    JSON = await Adress.get_errors(ORG)

    df = DataFrame(data=JSON)
    df = df.fillna('')
    if len(df) == 0:
        mess = 'пока не нашел ошибок'
        return await message.answer(mess)
    FILENAME = '/tmp/Адреса без номера дома.xlsx'
    SHETNAME = 'def'

    write_styling_excel(FILENAME, df, SHETNAME)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
    await Log.add(message['from']['id'], 29)
