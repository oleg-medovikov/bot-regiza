from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from clas import User
from func import delete_message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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

    kb_hello = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )
    kb_hello.add(InlineKeyboardButton(
        text='Да, требуется',
        callback_data='send_manual'
    ))

    kb_hello.add(InlineKeyboardButton(
        text='Нет, не требуется',
        callback_data='no_send_manual'
    ))
    mess = f"Добрый день, {USER.fio}!"
    mess += "\nВам требуется мануал, чтобы пользоваться мной?"
    return await message.answer(mess, reply_markup=kb_hello)


@dp.callback_query_handler(Text(equals=['send_manual']))
async def send_manual(query: types.CallbackQuery):
    kb_hello = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )
    kb_hello.add(InlineKeyboardButton(
        text='Нет, не требуется',
        callback_data='no_send_manual'
    ))
    await query.message.edit_reply_markup(reply_markup=kb_hello)
    return await query.message.answer('Серьезно?')


@dp.callback_query_handler(Text(equals=['no_send_manual']))
async def no_send_manual(query: types.CallbackQuery):
    kb_hello = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )
    kb_hello.add(InlineKeyboardButton(
        text='Да, требуется',
        callback_data='send_manual'
    ))

    await query.message.edit_reply_markup(reply_markup=kb_hello)
    return await query.message.answer('Ну и слава богу.')
