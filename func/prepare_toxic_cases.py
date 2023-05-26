from pandas import DataFrame
from datetime import datetime

from clas import ToxicCase


def check_biz_key(KEY: str, DICT: dict) -> dict:
    try:
        int(key)
    except ValueError:
        DICT['critical_error'] = True
        DICT['errors'] = DICT.get('errors', '') \
            + f'\n неправильный case_biz_key \n{KEY}'
    else:
        DICT['case_biz_key'] = int(key)
    return DICT


async def check_org_id(ORG_NAME: str, DICT: dict) -> dict:
    try:
        ORG_ID = await Organization.get_id(ORG_NAME)
    except ValueError as e:
        DICT['critical_error'] = True
        DICT['errors'] = DICT.get('errors', '') \
            + str(e)
    else:
        DICT['org_id'] = ORG_ID
    return DICT


async def check_integer(KEY: str, OBSER: int, DICT: dict) - dict:
    try:
        int(key)
    except ValueError:
        


async def prepare_toxic_cases(DF: DataFrame) -> list:
    "Превращаем таблицу данных в список ToxicCase"
    for row in df.to_dict('records'):
        DICT = {}
        DICT['critical_error'] = False
        # приступаем к проверке данных, сначала самое критичное
        DICT = check_biz_key(row['case_biz_key'], DICT)
        DICT = await check_org_id(row['medical_help_name'], DICT)
        if DICT['critical_error']:
            # если неправильный ключ или организация, то можно не продолжать
            continue

        # Простые вещи:
        DICT['history_number'] = row['history_number']
        DICT['sex'] = True if row['gender'] == "male" else False
        DICT['age'] = int(row['age'])
        DICT['mkb_id'] = await MKB.get_id(row['diagnosis'])
        DICT['diagnoz_date'] = row['date_aff_first']
        DICT['doc_smo'] = await Doctor.id(row['smo_fio'])
        DICT['doc_md'] = await Doctor.id(row['meddoc_fio'])

        # Даты отдельно
        DICT['o_303'] = datetime.strptime(row['303'], '%d.%m.%Y')
        DICT['o_1104'] = datetime.strptime(row['303'], '%d.%m.%Y')
        DICT['o_1105'] = datetime.strptime(row['303'], '%d.%m.%Y')


        TC = ToxicCase(**{
            'o_1101': int(row['1101']),
            'o_1103': row['1103'],
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


