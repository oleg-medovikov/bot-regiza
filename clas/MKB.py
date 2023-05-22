from pydantic import BaseModel
from datetime import datetime
from asyncpg.exceptions import DataError

from base import database, t_dict_mkb


class MKB(BaseModel):
    mkb_id:      int
    mkb_code:    str
    mkb_rpn:     str
    date_update: datetime

    @staticmethod
    async def get_id(MKB_code: str) -> int:
        query = t_dict_mkb.select(
            t_dict_mkb.c.mkb_code == MKB_code
        )

        res = await database.fetch_one(query)
        if res is not None:
            return res['mkb_id']
        else:
            raise ValueError(f'Не хватает МКБ в справочнике: {MKB_code}')

    @staticmethod
    async def get_all():
        query = t_dict_mkb.select().order_by(t_dict_mkb.c.mkb_id)
        list_ = []
        for row in await database.fetch_all(query):
            list_.append(MKB(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                'mkb_id': 0,
                'mkb_code': 'Z0.0',
                'mkb_rpn': '982347',
                'date_update':  datetime.now(),
            }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            row['mkb_rpn'] = str(row['mkb_rpn'])
            query = t_dict_mkb.select(
                t_dict_mkb.c.mkb_id == row['mkb_id']
                )
            res = await database.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                row['date_update'] = datetime.now()
                row.pop('mkb_id')
                query = t_dict_mkb.insert().values(**row)
                try:
                    await database.execute(query)
                except Exception as e:
                    string += f"ошибка в строчке {row['mkb_code']}\n {str(e)}"
                else:
                    string += f"добавил строку {row['mkb_code']}\n"
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    row['date_update'] = datetime.now()
                    query = t_dict_mkb.update()\
                        .where(
                            t_dict_mkb.c.mkb_id == row['mkb_id'])\
                        .values(**row)
                    try:
                        await database.execute(query)
                    except DataError:
                        string += f"ошибка в строчке {row['mkb_code']}\n"
                    else:
                        string += f"обновил строку {row['mkb_code']}\n"

                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
