from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from clas import User, ToxicCase, Organization, Log
from func import delete_message, send_large_message


class HistoryNumber(StatesGroup):
    number = State()


@dp.message_handler(commands=['search_history_number'])
async def ask_history_number(message: types.Message):
    "Начнем с того, что спросим номер"
    await delete_message(message)
    await message.answer("Введите номер истории болезни")
    await HistoryNumber.number.set()


@dp.message_handler(state=HistoryNumber.number)
async def load_history_number(message: types.Message, state: FSMContext):
    "читаем и обрабатываем номер истории"
    async with state.proxy() as data:
        data['number'] = message.text

        await state.finish()

        try:
            USER = await User.get(message['from']['id'])
        except ValueError:
            await Log.add(message['from']['id'], 2)
            return await message.answer('У вас нет прав на это действие')

        if USER.role in ['admin', 'rpn']:
            ORG = await Organization.get_org_id_list()
        else:
            ORG = [USER.org]

        JSON = await ToxicCase.search_history_number(data['number'], ORG)

        if len(JSON) == 0:
            await Log.add(message['from']['id'], 25)
            return await message.answer("Не нашел такого номера")

        mess = ''
        for row in JSON:
            mess += '=========================\n'
            for key, value in row.items():
                mess += f'{key}:  {value}\n'

        await Log.add(message['from']['id'], 24)
        return await send_large_message(message, mess)
