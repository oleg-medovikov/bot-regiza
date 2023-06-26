from pandas import DataFrame
from datetime import datetime

from clas import ToxicCase, DictObser, Organization, \
    MKB, Doctor, ToxicCaseError

from .get_rpn_age import get_rpn_age


def check_biz_key(KEY: str, DICT: dict) -> dict:
    try:
        DICT['case_biz_key'] = int(KEY)
    except ValueError:
        DICT['critical_error'] = True
        DICT['errors'] = DICT.get('errors', '') \
            + f'неправильный case_biz_key {KEY} \n'
    return DICT


async def check_org_id(ORG_NAME: str, DICT: dict) -> dict:
    try:
        DICT['org_id'] = await Organization.get_id(ORG_NAME)
    except ValueError as e:
        DICT['critical_error'] = True
        DICT['errors'] = DICT.get('errors', '') \
            + str(e)
    return DICT


async def check_integer(VALUE: str, OBSER: int, DICT: dict) -> dict:
    if VALUE is None or VALUE != VALUE or VALUE == '':
        DICT[f'o_{OBSER}'] = -1
        if OBSER not in [1112]:
            DICT['errors'] = DICT.get('errors', '') \
                + f'пустое значение показателя {OBSER}\n'
        return DICT

    try:
        DICT[f'o_{OBSER}'] = int(VALUE)
    except ValueError:
        try:
            DICT[f'o_{OBSER}'] = await DictObser.nsi_key_by_value(VALUE, OBSER)
        except ValueError:
            DICT[f'o_{OBSER}'] = -1
            DICT['errors'] = DICT.get('errors', '') \
                + f'неправильное значение в показателе {OBSER}: {VALUE}\n'
        else:
            DICT['errors'] = DICT.get('errors', '') \
                + f'значение вместо ключа в показателе {OBSER}\n'
    return DICT


def check_dates(DICT: dict) -> dict:
    if DICT['o_303'] > datetime.now():
        DICT['critical_error'] = True
        DICT['errors'] = DICT.get('errors', '') \
            + 'дата диагноза 303 больше текущей даты\n'

    if DICT['o_1104'] > DICT['o_303']:
        DICT['errors'] = DICT.get('errors', '') \
            + 'дата отравления 1104 позднее даты диагноза 303\n'

    if DICT['o_1105'] > DICT['o_303']:
        DICT['errors'] = DICT.get('errors', '') \
            + 'первичное обращения 1105 позднее даты диагноза 303\n'
    return DICT


async def check_distric(VALUE: str, DICT: dict) -> dict:
    if VALUE[0:2] == '41':
        DICT['o_1123'] = 1000
        DICT['errors'] = DICT.get('errors', '') \
            + 'Ленинградская область!\n'
        return DICT
    if VALUE == '40000000000':
        DICT['o_1123'] = 4000
        return DICT

    if VALUE[0:2] == '40':
        DICT['o_1123'] = int(VALUE[2:5])
        return DICT

    if VALUE == '0':
        DICT['o_1123'] = 0
        return DICT

    try:
        DICT['o_1123'] = await DictObser.nsi_key_by_value(VALUE, 1123)
    except ValueError:
        DICT['o_1123'] = 0
        DICT['errors'] = DICT.get('errors', '') \
            + f'неправильно передан район {VALUE}\n'

    return DICT


async def add_error(DICT: dict, ERROR: str):
    "записываем как ошибку в таблицу ошибок"
    TCE = ToxicCaseError(**{
        'case_biz_key':   DICT['case_biz_key'],
        'org_id':         DICT['org_id'],
        'history_number': DICT['history_number'],
        'mkb_id':         DICT['mkb_id'],
        'diagnoz_date':   DICT['diagnoz_date'],
        'doc_smo':        DICT['doc_smo'],
        'doc_md':         DICT['doc_md'],
        'error':          ERROR,

    })
    await TCE.add()


async def prepare_toxic_cases(DF: DataFrame) -> list:
    "Превращаем таблицу данных в список ToxicCase"
    LIST = []

    DF = DF.fillna('')

    for row in DF.to_dict('records'):
        DICT = {}
        DICT['critical_error'] = False
        DICT['errors'] = ''
        # приступаем к проверке данных, сначала самое критичное
        DICT = check_biz_key(row['case_biz_key'], DICT)
        DICT = await check_org_id(row['medical_help_name'], DICT)
        if DICT['critical_error']:
            # если неправильный ключ или организация, то можно не продолжать
            # и не нужно сохранять в ошибку
            continue

        # Простые вещи:
        DICT['history_number'] = row['history_number']
        DICT['is_cancelled'] = row['case_is_cancelled']
        DICT['sex'] = True if row['gender'] == "male" else False
        DICT['mkb_id'] = await MKB.get_id(row['diagnosis'])
        DICT['diagnoz_date'] = row['date_aff_first']
        DICT['doc_smo'] = await Doctor.id(row['smo_fio'])
        DICT['doc_md'] = await Doctor.id(row['meddoc_fio'])
        DICT['o_1102'] = row['1102']
        DICT['o_1103'] = row['1103']
        DICT['o_1107'] = row['1107']
        DICT['o_1111'] = row['1111']
        DICT['o_1116'] = row['1116']
        DICT['o_1118'] = row['1118']

        # Даты отдельно
        try:
            DICT['o_303'] = datetime.strptime(row['303'], '%d.%m.%Y')
            DICT['o_1104'] = datetime.strptime(row['1104'], '%d.%m.%Y')
            DICT['o_1105'] = datetime.strptime(row['1105'], '%d.%m.%Y')
        except TypeError:
            await add_error(DICT, 'одна из дат 303, 1104, 1105 пустая')
            continue
        except ValueError:
            mess = 'даты 303, 1104, 1105 неверного формата \n'
            mess += f"303:{row['303']}\n 1104:{row['1104']}\n 1105:{row['1105']}"
            await add_error(DICT, mess)
            continue
        DICT = check_dates(DICT)
        if DICT['critical_error']:
            await add_error(DICT, DICT['errors'])
            continue

        # расчитываем возраст
        DICT['age'] = get_rpn_age(row['case_patient_birthdate'], DICT['o_303'])

        # Проверка ключей словарей
        LIST_OBSER = [
            1101, 1106, 1108, 1109, 1110, 1112, 1113, 1114, 1115, 1117, 1119
        ]

        for OBSER in LIST_OBSER:
            DICT = await check_integer(row[str(OBSER)], OBSER, DICT)

        # на последок - районы
        DICT = await check_distric(row['1123'], DICT)

        LIST.append(ToxicCase(**DICT))
    return LIST
