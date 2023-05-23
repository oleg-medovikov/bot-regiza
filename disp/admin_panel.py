from .dispetcher import dp
from aiogram import types
from pandas import DataFrame
import os

from clas import User, MKB, Organization, DictObser
from func import delete_message, write_styling_excel

MESS = """*Доступные команды для редактирования базы*

    /get_users
    /get_mkb
    /get_organizations
    /get_dict_obser

    *Выгрузка данных их нетрики*
    /get_cases
    """.replace('_', '\\_')


@dp.message_handler(commands=['admin_panel'])
async def admin_panel(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы не являетесь админом",
            parse_mode='html'
            )

    return await message.answer(MESS, parse_mode='Markdown')

DICT_XLSX = [
    'get_users',
    'get_mkb',
    'get_organizations',
    'get_dict_obser',
]


@dp.message_handler(commands=DICT_XLSX)
async def send_objects_file(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы не являетесь админом",
            parse_mode='html'
            )
    COMMAND = message.text.replace('/', '')

    JSON = {
        'get_users':         User.get_all(),
        'get_mkb':           MKB.get_all(),
        'get_organizations': Organization.get_all(),
        'get_dict_obser':    DictObser.get_all(),
    }.get(COMMAND)

    df = DataFrame(data=await JSON)
    df['date_update'] = df['date_update'].dt.strftime('%H:%M  %d.%m.%Y')
    FILENAME = f'/tmp/{COMMAND[4:]}.xlsx'
    SHETNAME = 'def'

    write_styling_excel(FILENAME, df, SHETNAME)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
