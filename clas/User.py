from sqlalchemy.sql.expression import values
from pydantic import BaseModel, Field

from base import database, t_users, t_people


class User (BaseModel):
    u_id : int
    first_name : str
    last_name : str
    username : str

    async def add(USER): 
        "Добавление пользователя в таблицу пользователей"

        query = t_users.select(t_users.c.u_id == USER.id)

        res = await database.fetch_one(query)

        if not res is None:
            return 'Есть такой юзер'
        else:
            values = {
                    'u_id' : USER.id,
                    'first_name' : USER.first_name,
                    'last_name' : USER.last_name,
                    'username' : USER.username
                    }
            query = t_users.insert().values(**values)
            
            await database.execute(query)
    
    async def add_people(USER):
        "Добавим людей которые писали боту"
        query = t_people.select(t_people.c.u_id == USER.id)

        res = await database.fetch_one(query)

        if res is None:
            values = {
                    'u_id' : USER.id,
                    'first_name' : USER.first_name,
                    'last_name' : USER.last_name,
                    'username' : USER.username
                    }
            query = t_people.insert().values(**values)
            
            await database.execute(query)


    async def check(USER) -> bool:
        "Проверка пользователя на наличие в базе"

        query = t_users.select(t_users.c.u_id == USER.id)
        
        res = await database.fetch_one(query)

        if not res is None:
            return True
        else:
            return False
 
