from .dispetcher import dp
from aiogram import types
import os

from clas import User, ToxicCase
from func import delete_message, write_styling_excel

MESS = """*Формируем файлы статистики и сводные отчеты*

    *Свод отравлений по районам*
        Количество поставленых токсикологических диагнозов
    за текущий год, в разрезе районов СПб и месяцев.
    /svod_toxic_district
       """.replace('_', '\\_')


@dp.message_handler(commands=['statistic_panel'])
async def statistic_panel(message: types.Message):
    await delete_message(message)

    try:
        await User.get(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы неизвестный пользователь",
            parse_mode='html'
            )

    return await message.answer(MESS, parse_mode='Markdown')

DICT_XLSX = [
    'svod_toxic_district',
]


@dp.message_handler(commands=DICT_XLSX)
async def send_statistic_file(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы неизвестный пользователь",
            parse_mode='html'
            )
    COMMAND = message.text.replace('/', '')

    JSON = {
        'svod_toxic_district': ToxicCase.svod_toxic_district(),
    }.get(COMMAND)

    df = await JSON
    FILENAME = f'/tmp/{COMMAND[4:]}.xlsx'
    SHETNAME = 'def'

    write_styling_excel(FILENAME, df, SHETNAME, True)
    #df.to_excel(FILENAME)
    await message.answer_document(open(FILENAME, 'rb'))
    os.remove(FILENAME)
