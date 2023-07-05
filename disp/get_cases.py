from .dispetcher import dp
from aiogram import types
from datetime import datetime, timedelta

from func import delete_message, toxic_get_cases, prepare_toxic_cases
from clas import User, Organization, Log


@dp.message_handler(commands=['get_cases'])
async def get_cases(message: types.Message):
    """выгрузка за текущий год"""
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 1)
        return await message.answer(
            "Вы не являетесь админом",
            parse_mode='html'
            )
    # берем список актуальных организаций
    ORGS = await Organization.get_org_list()
    END = datetime.today()
    START = END - timedelta(days=365)

    try:
        df = toxic_get_cases(
            START.strftime('%Y-%m-%d'),
            END.strftime('%Y-%m-%d'),
            ORGS
        )
    except Exception as e:
        return await message.answer(
            str(e),
            parse_mode='Markdown'
        )

    mess = f'Размер датафрейма за месяц c {START.strftime("%Y-%m-%d")}'
    mess += f': {len(df)}'
    mess += '\n\n'

    count_add = 0
    count_cancel = 0

    for TC in await prepare_toxic_cases(df):
        try:
            await TC.add()
        except Exception as e:
            mess += str(e)
        else:
            # await ToxicCaseError.delete(TC.case_biz_key)
            if TC.is_cancelled:
                count_cancel += 1
            else:
                count_add += 1

    mess += f'Добавлено случаев: {count_add}\n'
    mess += f'Отмененные случаи: {count_cancel}\n'
    await Log.add(message['from']['id'], 23)
    return await message.answer(mess, parse_mode='Markdown')
