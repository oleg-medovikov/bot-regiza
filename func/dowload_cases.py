from pandas import DataFrame, to_datetime
import requests
from json.decoder import JSONDecodeError

from conf import REGIZ_TOKEN, REGIZ_URL


class my_except(Exception):
    pass


def toxic_get_cases(START: str, END: str, ORGS: list) -> 'DataFrame':
    """чаем начальную выборку"""
    URL = REGIZ_URL + f"?id=1218&args={START},{END}&auth={REGIZ_TOKEN}"

    req = requests.get(URL)
    if req.status_code != 200:
        raise my_except('Недоступен сервер нетрики, попробуйте позже \n' + URL)

    try:
        df = DataFrame(data=req.json())
    except JSONDecodeError:
        raise my_except('Недоступен сервер нетрики, попробуйте позже')
    except requests.Timeout:
        raise my_except('Недоступен сервер нетрики, попробуйте позже')
    except requests.ConnectionError:
        raise my_except('Недоступен сервер нетрики, попробуйте позже')

    df = df.loc[df['medical_help_name'].isin(ORGS)]

    if len(df) == 0:
        raise my_except('нет случаев!')

    # Распознаем автоматические даты создания МК и показателей
    df['date_aff_first'] = to_datetime(
        df['date_aff_first'],
        format='%Y-%m-%d %H:%M:%S'
        )
    # Сортируем по датам и удаляем дублирующиеся строки,
    # оставляя последнее изменение
    df.sort_values(by=['date_aff_first'], inplace=True)
    # df.drop_duplicates(
    #    subset=df.columns.drop('date_aff_first'),
    #    keep='last',
    #    inplace=True
    #    )
    # исправляем индексы
    df.index = range(len(df))

    # делаем разворот таблицы для показателей
    obs = df.pivot_table(
        index=['case_biz_key', 'case_is_cancelled'],
        columns=['observation_code'],
        values=['observation_value'],
        aggfunc='first'
        ).stack(0)
    try:
        obs.loc[obs['303'].isnull(), '303'] = obs.loc[obs['303'].isnull(), '1749']
    except KeyError:
        obs['303'] = obs['1749']

    # уникальные строки по номеру истории болезни
    DF = df.copy()

    del DF['observation_code']
    del DF['observation_value']

    DF.drop_duplicates(
        subset=['case_biz_key', 'case_is_cancelled'],
        keep='last',
        inplace=True
    )

    # соединяем уникальные истории с показателями
    DF = DF.merge(obs, how='left', on=['case_biz_key', 'case_is_cancelled'])
    # обновляем индексы
    DF.index = range(len(DF))

    # добавляем поля, если каких-то обсервов не хватает
    CASE_CODES = [
        '303', '1101', '1102', '1103',
        '1104', '1105', '1106', '1107',
        '1108', '1109', '1110', '1111',
        '1112', '1113', '1114', '1115',
        '1116', '1117', '1118', '1119',
        '1123'
        ]

    for CASE in CASE_CODES:
        if CASE not in DF.columns:
            DF[CASE] = ''

    return DF
