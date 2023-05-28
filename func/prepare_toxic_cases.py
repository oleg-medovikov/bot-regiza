from pandas import DataFrame
from datetime import datetime

from clas import ToxicCase, DictObser, Organization, \
    MKB, Doctor


def check_biz_key(KEY: str, DICT: dict) -> dict:
    try:
        DICT['case_biz_key'] = int(KEY)
    except ValueError:
        DICT['critical_error'] = True
        DICT['errors'] = DICT.get('errors', '') \
            + f'\n неправильный case_biz_key \n{KEY}'
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
    if VALUE is None or VALUE != VALUE:
        DICT[f'o_{OBSER}'] = -1
        DICT['errors'] = DICT.get('errors', '') \
            + f'\n пустое значение показателя {OBSER}'
        return DICT

    try:
        DICT[f'o_{OBSER}'] = int(VALUE)
    except ValueError:
        try:
            DICT[f'o_{OBSER}'] = await DictObser.nsi_key_by_value(VALUE, OBSER)
        except ValueError:
            DICT[f'o_{OBSER}'] = -1
            DICT['errors'] = DICT.get('errors', '') \
                + f'\n неправильное значение в показателе {OBSER}: {VALUE}'
        else:
            DICT['errors'] = DICT.get('errors', '') \
                + f'\n значение вместо ключа в показателе {OBSER}'
    return DICT


def check_dates(DICT: dict) -> dict:
    if DICT['o_303'] > datetime.now():
        DICT['errors'] = DICT.get('errors', '') \
            + '\n дата диагноза 303 больше текущей даты'

    if DICT['o_1104'] > DICT['o_303']:
        DICT['errors'] = DICT.get('errors', '') \
            + '\n дата отравления 1104 позднее даты диагноза 303'

    if DICT['o_1105'] > DICT['o_303']:
        DICT['errors'] = DICT.get('errors', '') \
            + '\n первичное обращения 1105 позднее даты диагноза 303'
    return DICT


async def check_distric(VALUE: str, DICT: dict) -> dict:
    try:
        DICT['o_1123'] = await DictObser.nsi_key_by_rpn_key(VALUE, 1123)
    except ValueError:
        DICT['o_1123'] = 0
        DICT['errors'] = DICT.get('errors', '') \
            + '\n неправильно передан район'
    return DICT


async def prepare_toxic_cases(DF: DataFrame) -> list:
    "Превращаем таблицу данных в список ToxicCase"
    LIST = []

    for row in DF.to_dict('records'):
        DICT = {}
        DICT['critical_error'] = False
        DICT['errors'] = ''
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
        DICT['o_1102'] = row['1102']
        DICT['o_1103'] = row['1103']
        DICT['o_1107'] = row['1107']
        DICT['o_1116'] = row['1116']
        DICT['o_1118'] = row['1118']

        # Даты отдельно
        try:
            DICT['o_303'] = datetime.strptime(row['303'], '%d.%m.%Y')
            DICT['o_1104'] = datetime.strptime(row['1104'], '%d.%m.%Y')
            DICT['o_1105'] = datetime.strptime(row['1105'], '%d.%m.%Y')
        except TypeError:
            continue
        except ValueError:
            continue
        DICT = check_dates(DICT)

        # Проверка ключей словарей
        LIST_OBSER = [
            1101, 1106, 1108, 1109, 1110, 1113, 1114, 1115, 1117, 1119
        ]

        for OBSER in LIST_OBSER:
            DICT = await check_integer(row[str(OBSER)], OBSER, DICT)

        # на последок - районы
        DICT = await check_distric(row['1123'], DICT)

        LIST.append(ToxicCase(**DICT))
    return LIST
