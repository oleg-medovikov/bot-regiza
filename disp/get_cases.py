from .dispetcher import dp
from aiogram import types
from datetime import datetime

from func import delete_message, toxic_get_cases, prepare_toxic_cases
from clas import User, Organization


@dp.message_handler(commands=['get_cases'])
async def get_cases(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы не являетесь админом",
            parse_mode='html'
            )
    # берем список актуальных организаций
    ORGS = await Organization.get_org_list()

    try:
        df = toxic_get_cases('2023-03-01', '2023-06-01', ORGS)
    except Exception as e:
        return await message.answer(str(e), parse_mode='Markdown')

    mess = f'Размер датафрейма {len(df)} \n\n'

    for TC in await prepare_toxic_cases(df):
        try:
            await TC.add()
        except Exception as e:
            mess += str(e)
            break

    return await message.answer(mess, parse_mode='Markdown')
