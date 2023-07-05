from .dispetcher import dp, bot
from aiogram import types
import os
import pandas as pd

from clas import User, MKB, Organization, DictObser, Log
from func import delete_message, send_large_message

NAMES = {
    'users.xlsx': ['u_id', 'fio', 'org', 'role', 'date_update'],
    'mkb.xlsx': ['mkb_id', 'mkb_code', 'mkb_rpn', 'date_update'],
    'organizations.xlsx': ['org_id', 'org_biz_key', 'org_name', 'date_update'],
    'dict_obser.xlsx': [
        'id', 'obs_code', 'obs_name', 'nsi_key',
        'rpn_key', 'value', 'date_update'
        ],
        }


@dp.message_handler(content_types='document')
async def update_base(message: types.Message):
    """Работа с файлами которые посылает пользователь"""
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 1)
        return await message.answer(
            "вы не являетесь админом",
            parse_mode='html'
            )

    FILE = message['document']

    if not FILE['file_name'] in NAMES.keys():
        await Log.add(message['from']['id'], 3)
        return await message.answer('У файла неправильное имя')

    DESTINATION = '/tmp/' + FILE.file_unique_id + 'xlsx'

    await bot.download_file_by_id(
        file_id=FILE.file_id,
        destination=DESTINATION
        )

    COLUMNS = NAMES.get(FILE['file_name'])
    try:
        df = pd.read_excel(DESTINATION, usecols=COLUMNS)
    except Exception as e:
        await Log.add(message['from']['id'], 4)
        os.remove(DESTINATION)
        return await message.answer(str(e))

    for col in df.columns:
        try:
            df[col] = df[col].str.replace('\u2028', '\n')
            df[col] = df[col].str.replace("'", '"')
        except AttributeError:
            continue

    list_ = df.to_dict('records')

    MESS, ACTION = {
        'users':         (User.update_all(list_), 61),
        'mkb':           (MKB.update_all(list_), 62),
        'organizations': (Organization.update_all(list_), 63),
        'dict_obser':    (DictObser.update_all(list_), 64),
        }.get(FILE['file_name'][:-5])

    try:
        MESS = await MESS
    except TypeError as e:
        MESS = 'Пока не могу этот файл обработать\n' + str(e)

    await send_large_message(message, MESS)
    os.remove(DESTINATION)
    await Log.add(message['from']['id'], ACTION)
