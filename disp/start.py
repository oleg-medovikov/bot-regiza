from .dispetcher import dp
from aiogram import types

from clas import User
from func import delete_message


@dp.message_handler(commands=['start', 'старт'])
async def send_welcome(message: types.Message):
    await delete_message(message)

    try:
        USER = await User.get(message['from']['id'])
    except ValueError:
        return await message.answer(
            f"неизвестный юзер {message['from']['id']}",
            parse_mode='html'
            )

    return await message.answer("Добрый день " + USER.fio, parse_mode='html')
