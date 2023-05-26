from .dispetcher import dp
from aiogram import types
from datetime import datetime

from func import delete_message, toxic_get_cases
from clas import User, Organization, Doctor, MKB, ToxicCase


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
        df = toxic_get_cases('2023-05-01', '2023-05-05', ORGS)
    except Exception as e:
        return await message.answer(str(e), parse_mode='Markdown')

    mess = f'Размер датафрейма {len(df)} \n\n'

    for row in df.to_dict('records'):
        TC = ToxicCase(**{
            'case_biz_key': int(row['case_biz_key']),
            'org_id': await Organization.get_id(row['medical_help_name']),
            'history_number': row['history_number'],
            'sex': True if row['gender'] == "male" else False,
            'age': int(row['age']),
            'mkb_id': await MKB.get_id(row['diagnosis']),
            'diagnoz_date': row['date_aff_first'],
            'doc_smo': await Doctor.id(row['smo_fio']),
            'doc_md': await Doctor.id(row['meddoc_fio']),
            'o_303': datetime.strptime(row['303'], '%d.%m.%Y'),
            'o_1101': int(row['1101']),
            'o_1103': row['1103'],
            'o_1104': datetime.strptime(row['1104'], '%d.%m.%Y'),
            'o_1105': datetime.strptime(row['1105'], '%d.%m.%Y'),
            'o_1106': int(row['1106']),
            'o_1107': row['1107'],
            'o_1108': int(row['1108']),
            'o_1109': int(row['1109']),
            'o_1110': int(row['1110']),
            'o_1113': int(row['1113']),
            'o_1114': int(row['1114']),
            'o_1115': int(row['1115']),
            'o_1116': row['1116'],
            'o_1117': int(row['1117']),
            'o_1118': row['1118'],
            'o_1119': int(row['1119']),
            'o_1123': row['1123'],
            'errors': '',
        })

        await TC.add()

    return await message.answer(mess, parse_mode='Markdown')
