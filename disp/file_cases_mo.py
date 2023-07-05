from .dispetcher import dp
from pandas import DataFrame
from aiogram import types
from datetime import datetime
import os
from aiogram_calendar import simple_cal_callback, SimpleCalendar


from func import delete_message, return_month, \
    write_styling_excel, month_name, create_xml
from clas import User, ToxicCase, Organization, Log


@dp.message_handler(commands=['file_get_toxic_cases'])
async def file_get_toxic_cases(message: types.Message):
    await delete_message(message)

    try:
        await User.get(message['from']['id'])
    except ValueError:
        await Log.add(message['from']['id'], 2)
        return await message.answer(
            "вы неизвестный пользователь!",
            parse_mode='html'
            )
    await message.answer(
        text="Выбор даты:",
        reply_markup=await SimpleCalendar().start_calendar(
            datetime.now().year,
            datetime.now().month
            )
        )


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(
        callback_query: types.CallbackQuery,
        callback_data: dict):
    """Создание задания после выбора даты из календаря"""

    selected, date = await SimpleCalendar().process_selection(
            callback_query,
            callback_data)

    if selected:
        await delete_message(callback_query.message)

        USER = await User.get(callback_query['from']['id'])
        if USER.role in ['admin', 'rpn']:
            MO = await Organization.get_org_id_list()
        else:
            MO = [USER.org]
        START, END = return_month(date)

        JSON = await ToxicCase.file_cases_mo(START, END, MO)

        df = DataFrame(data=JSON)
        df = df.fillna('')
        if len(df) == 0:
            mess = f'Нет случаев за месяц {month_name(date.month)}' \
                + f' {date.year} года'
            return await callback_query.message.answer(mess)
        FILENAME = f'/tmp/Случаи_за_{month_name(date.month)}_{date.year}.xlsx'
        SHETNAME = 'def'

        write_styling_excel(FILENAME, df, SHETNAME)
        await callback_query.message.answer_document(open(FILENAME, 'rb'))
        os.remove(FILENAME)
        await Log.add(USER.u_id, 21)

        # Создаем файлик XML
        if USER.role in ['admin', 'rpn']:
            # за месяц
            JSON = await ToxicCase.file_cases_xml(START, END)
            NAME = f'Случаи_за_{month_name(date.month)}_{date.year}'
            FILE = create_xml(JSON, NAME)
            await callback_query.message.answer_document(open(FILE, 'rb'))

            # за день
            JSON = await ToxicCase.file_cases_xml(date, date)
            NAME = f'Случаи_за_{date.strftime("%d_%m_%Y")}'
            FILE = create_xml(JSON, NAME)
            await callback_query.message.answer_document(open(FILE, 'rb'))
