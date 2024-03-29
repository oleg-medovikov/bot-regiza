from .dispetcher import dp
from aiogram import types
from pandas import DataFrame
import os

from clas import User, MKB, Organization, DictObser, Log
from func import delete_message, write_styling_excel

MESS = """*Доступные команды для редактирования базы*

    /get_users
    /get_mkb
    /get_organizations
    /get_dict_obser

    *Посмотреть лог пользователей*
    кто и как пользовался ботом
    /get_logs

    *Сверка адресов в яндекс геокодер*
    /process_adresses
    *Скопом переделать квартиры*
    /process_flat

    *Выгрузка данных из нетрики*
    скопом выгрузить данные с текущей даты и на 365 дней назад
    /get_cases

    """.replace('_', '\\_')


@dp.message_handler(commands=['admin_panel'])
async def admin_panel(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 1)
        return await message.answer(
            "вы не являетесь админом",
            parse_mode='html'
            )

    return await message.answer(MESS, parse_mode='Markdown')

DICT_XLSX = {
    'get_users':         11,
    'get_mkb':           12,
    'get_organizations': 13,
    'get_dict_obser':    14,
}


@dp.message_handler(commands=DICT_XLSX.keys())
async def send_objects_file(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 1)
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
    await Log.add(message['from']['id'], DICT_XLSX.get(COMMAND))
