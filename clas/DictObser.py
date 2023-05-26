from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import and_
from asyncpg.exceptions import DataError

from base import database, t_dict_obser


class DictObser(BaseModel):
    id:          int
    obs_code:     int
    obs_name:     str
    nsi_key:     int
    rpn_key:     str
    value:       str
    date_update: datetime

    @staticmethod
    async def nsi_key_by_value(VALUE: str, OBSER: int) -> int:
        "пробуем найти значение ключа по слову"
        query = t_dict_obser.select().where(and_(
            t_dict_obser.c.obs_code == OBSER,
            t_dict_obser.c.value == VALUE
            ))
        res = await database.fetch_one(query)
        if res is None:
            raise ValueError
        else:
            return res['nsi_key']

    @staticmethod
    async def gen_dict_nsi(OBSER: int) -> dict:
        "генерируем конкретный словарь для обсервейшена"
        query = t_dict_obser.select().where(
            t_dict_obser.c.obs_code == OBSER
        )
        DICT = {}
        for ROW in await database.fetch_all(query):
            DICT[ROW['nsi_key']] = ROW['nsi_key']
            DICT[ROW['value']] = ROW['nsi_key']
        return DICT

    @staticmethod
    async def get_all():
        query = t_dict_obser.select().order_by(t_dict_obser.c.id)
        list_ = []
        for row in await database.fetch_all(query):
            list_.append(DictObser(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                'id':          0,
                'ob_code':     222,
                'ob_name':     'test',
                'nsi_key':     2,
                'rpn_key':     '2356000',
                'value':       'какое-то значение',
                'date_update': datetime.now(),
            }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            row['rpn_key'] = str(row['rpn_key'])
            query = t_dict_obser.select(
                t_dict_obser.c.id == row['id']
                )
            res = await database.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                row['date_update'] = datetime.now()
                ID = row['id']
                row.pop('id')
                query = t_dict_obser.insert().values(**row)
                try:
                    await database.execute(query)
                except Exception as e:
                    string += f"ошибка в строчке {ID}\n {str(e)}"
                else:
                    string += f"добавил строку {ID}\n"
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    row['date_update'] = datetime.now()
                    query = t_dict_obser.update()\
                        .where(
                            t_dict_obser.c.id == row['id'])\
                        .values(**row)
                    try:
                        await database.execute(query)
                    except DataError:
                        string += f"ошибка в строчке {row['id']}\n"
                    else:
                        string += f"обновил строку {row['id']}\n"

                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
