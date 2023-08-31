from pydantic import BaseModel

from base import database, t_adress, t_toxic_cases
from sqlalchemy import select, desc, and_
from sqlalchemy.sql.expression import true


class Adress(BaseModel):
    line:    str
    point:   list
    text:    str
    street:  str
    house:   str
    flat:    str
    index:   int
    error:   bool

    @staticmethod
    async def get(LINE: str) -> 'Adress':
        query = t_adress.select(
                t_adress.c.line == LINE
                )
        res = await database.fetch_one(query)
        if res is None:
            raise ValueError('Нет такого адреса')
        return Adress(**res)

    async def add(self) -> None:
        query = t_adress.insert().values(**self.dict())
        await database.execute(query)

    @staticmethod
    async def get_errors(ORG: list) -> list:
        j = t_toxic_cases.join(
                t_adress,
                t_toxic_cases.c.o_1102 == t_adress.c.line,
                isouter=True
                )

        query = select([
            (t_toxic_cases.c.o_303).label('Дата установления диагноза (303)'),
            (t_toxic_cases.c.history_number).label('Номер истории болезни'),
            (t_toxic_cases.c.o_1102).label('Адрес места происшествия (1102)'),
            (t_adress.c.text).label('Адрес обработанный геокодером'),
            (t_adress.c.street).label('Улица'),
            (t_adress.c.house).label('Дом'),
            (t_adress.c.flat).label('Квартира'),
            ]).order_by(desc(t_toxic_cases.c.o_303)).select_from(j).where(and_(
                    t_adress.c.house == '',
                    t_toxic_cases.c.org_id.in_(ORG)
                    ))
        res = await database.fetch_all(query)
        return [dict(_) for _ in res]

    @staticmethod
    async def get_empty_adress() -> list:
        j = t_toxic_cases.join(
                t_adress,
                t_toxic_cases.c.o_1102 == t_adress.c.line,
                isouter=True
                )

        query = select([
            t_toxic_cases.c.o_1102
            ]).order_by(desc(t_toxic_cases.c.o_303)).select_from(j).where(
                    t_adress.c.line.is_(None)
                    )

        res = await database.fetch_all(query)
        return [_['o_1102'] for _ in res]

    @staticmethod
    async def get_all() -> list:
        query = t_adress.select()
        res = await database.fetch_all(query)
        return [Adress(**_) for _ in res]

    async def update(self) -> None:
        query = t_adress.update().where(
                t_adress.c.line == self.line
                ).values(**self.dict())
        await database.execute(query)
