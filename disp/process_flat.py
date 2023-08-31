from .dispetcher import dp
from aiogram import types

from func import delete_message, find_flat
from clas import User, Log, Adress


@dp.message_handler(commands=['process_flat'])
async def process_flat(message: types.Message):
    """скопом переделываем поиск квартиры"""
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 1)
        return await message.answer(
            "Вы не являетесь админом",
            parse_mode='html'
            )

    for ADRESS in await Adress.get_all():
        ADRESS.flat = find_flat(ADRESS.line)
        await ADRESS.update()

    mess = 'Закончил!'
    return await message.answer(mess, parse_mode='Markdown')
