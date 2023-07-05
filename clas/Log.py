from pydantic import BaseModel
from datetime import datetime

from base import database, t_logi


class Log(BaseModel):
    time:   datetime
    u_id:   int
    action: int

    @staticmethod
    async def add(U_ID: int, ACTION: int):
        "Записываем событие"
        sql = t_logi.insert().values({
            'time': datetime.now(),
            'u_id': U_ID,
            'action': ACTION
                })
        await database.execute(sql)
