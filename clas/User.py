from pydantic import BaseModel
from datetime import datetime

from base import database, t_users


class User (BaseModel):
    u_id:        int
    fio:         str
    org:         str
    role:        str
    date_create: datetime

    async def add(self):
        "Добавление пользователя в таблицу пользователей"

        query = t_users.select(t_users.c.u_id == self.u_id)
        res = await database.fetch_one(query)

        if res is not None:
            return 'Есть такой юзер'
        else:
            query = t_users.insert().values(self.__dict__)
            await database.execute(query)

    @staticmethod
    async def get(U_ID: int) -> 'User':
        "Вытаскиваем пользователя по id"
        query = t_users.select(t_users.c.u_id == U_ID)
        res = await database.fetch_one(query)

        if res is None:
            raise ValueError("Неизвестный U_ID!")

        return User(**res)

    async def check(self) -> bool:
        "Проверка пользователя на наличие в базе"

        query = t_users.select(t_users.c.u_id == self.__dict__)
        res = await database.fetch_one(query)

        if not res is None:
            return True
        else:
            return False
