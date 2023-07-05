from pydantic import BaseModel
from datetime import datetime

from base import database, t_logi, t_dict_obser, t_users, t_dict_orgs
from sqlalchemy import select, and_, desc


class Log(BaseModel):
    time:   datetime
    u_id:   int
    action: int

    @staticmethod
    async def add(U_ID: int, ACTION: int):
        "Записываем событие"
        query = t_logi.insert().values({
            'time': datetime.now(),
            'u_id': U_ID,
            'action': ACTION
                })
        await database.execute(query)

    @staticmethod
    async def get() -> list:
        "Выдаем все логи"
        j = t_logi.join(
            t_users,
            t_logi.c.u_id == t_users.c.u_id,
            isouter=True
        ).join(
            t_dict_obser,
            and_(
                t_logi.c.action == t_dict_obser.c.nsi_key,
                t_dict_obser.c.obs_code == 3
                ),
            isouter=True
        ).join(
            t_dict_orgs,
            t_users.c.org == t_dict_orgs.c.org_id
                )

        query = select([
            t_logi.c.time.label('Время события'),
            t_dict_orgs.c.org_name.label('Организация'),
            t_logi.c.u_id.label('Telegram id'),
            t_users.c.fio.label('ФИО'),
            t_logi.c.action.label('id события'),
            t_dict_obser.c.value.label('Событие'),
            ]).select_from(j).order_by(desc(t_logi.c.time))
        res = await database.fetch_all(query)
        return [dict(r) for r in res]
