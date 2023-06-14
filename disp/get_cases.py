from .dispetcher import dp
from aiogram import types
from datetime import datetime

from func import delete_message, toxic_get_cases, prepare_toxic_cases, \
    return_month, month_name
from clas import User, Organization

from aiogram_calendar import simple_cal_callback, SimpleCalendar


@dp.message_handler(commands=['get_cases'])
async def get_cases_ask_month(message: types.Message):
    await delete_message(message)

    try:
        await User.admin(message['from']['id'])
    except ValueError:
        return await message.answer(
            "вы не являетесь админом",
            parse_mode='html'
            )
    await message.answer(
        text="Выбор месяца:",
        reply_markup=await SimpleCalendar().start_calendar(
            datetime.now().year,
            datetime.now().month
            )
        )


@dp.callback_query_handler(simple_cal_callback.filter())
async def get_cases(
        callback_query: types.CallbackQuery,
        callback_data: dict):
    """Создание задания после выбора даты из календаря"""

    selected, date = await SimpleCalendar().process_selection(
            callback_query,
            callback_data
    )

    if selected:
        await delete_message(callback_query.message)

        # берем список актуальных организаций
        ORGS = await Organization.get_org_list()
        START, END = return_month(date)

        try:
            df = toxic_get_cases(
                START.strftime('%Y-%m-%d'),
                END.strftime('%Y-%m-%d'),
                ORGS
            )
        except Exception as e:
            return await callback_query.message.answer(
                str(e),
                parse_mode='Markdown'
            )

        mess = f'Размер датафрейма за месяц {month_name(date.month)} {len(df)}'
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

        return await callback_query.message.answer(mess, parse_mode='Markdown')
