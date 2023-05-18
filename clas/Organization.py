from pydantic import BaseModel
from datetime import datetime
from asyncpg.exceptions import DataError
from uuid import UUID

from base import database, t_dict_orgs


class Organization(BaseModel):
    org_id:         int
    org_biz_key:    UUID
    org_name:       str
    date_update: datetime

    @staticmethod
    async def get_id(BIZ_KEY: str) -> int:
        query = t_dict_orgs.select(
            t_dict_orgs.c.org_biz_key == BIZ_KEY
        )

        res = await database.fetch_one(query)
        if res is not None:
            return res['org_id']
        else:
            raise ValueError(f'Не хватает МО в справочнике: {BIZ_KEY}')

    @staticmethod
    async def get_all():
        query = t_dict_orgs.select().order_by(t_dict_orgs.c.org_id)
        list_ = []
        for row in await database.fetch_all(query):
            list_.append(Organization(**row).dict())

        if len(list_):
            return list_
        else:
            return [{
                'org_id':      0,
                'org_biz_key': 'ГУИД',
                'org_name':    'СПб ГБУЗ "Арбуз"',
                'date_update':  datetime.now(),
            }]

    @staticmethod
    async def update_all(list_: list) -> str:
        "Обновление всей таблицы"
        if len(list_) == 0:
            return 'Нечего обновлять'
        string = ''
        for row in list_:
            query = t_dict_orgs.select(
                t_dict_orgs.c.org_id == row['org_id']
                )
            res = await database.fetch_one(query)

            # если строки нет, то добавляем
            if res is None:
                string += f"добавил {row['org_name']}\n"
                row['date_update'] = datetime.now()
                row.pop('org_id')
                query = t_dict_orgs.insert().values(**row)
                await database.execute(query)
                continue

            # если строчка есть ищем несовпадение значений, чтобы заменить
            for key, value in dict(res).items():
                if row[key] != value and key != 'date_update':
                    string += f"обновил {row['org_name']}\n"
                    row['date_update'] = datetime.now()
                    query = t_dict_orgs.update()\
                        .where(
                            t_dict_orgs.c.org_id == row['org_id'])\
                        .values(**row)
                    try:
                        await database.execute(query)
                    except DataError:
                        string += f"ошибка в {row['org_name']}\n"

                    break
        if string == '':
            string = 'Нечего обновлять'
        return string
