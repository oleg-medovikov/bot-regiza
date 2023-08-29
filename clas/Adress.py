from pydantic import BaseModel

from base import database, t_adress, t_toxic_cases
from sqlalchemy import select, desc


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
    async def get_empty_adress() -> 'list':
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
