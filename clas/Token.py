from pydantic import BaseModel
from datetime import date

from base import database, t_tokens
from sqlalchemy import false


class Token(BaseModel):
    token:     str
    name:      str
    end:       bool
    end_date:  date
    count:     int

    @staticmethod
    async def get() -> 'Token':
        query = t_tokens.select(
                t_tokens.c.end == false()
                )
        res = await database.fetch_one(query)

        if res is None:
            raise ValueError('Нет доступного токена!')

        return Token(**res)

    async def update(self):
        query = t_tokens.update().where(
                t_tokens.c.token == self.token
                ).values(**self.dict())
        await database.execute(query)
