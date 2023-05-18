from pydantic import BaseModel
from datetime import datetime

from base import database, t_dict_doctor


class Doctor (BaseModel):
    doc_id:      int
    doc_fio:     str
    date_update: datetime

    @staticmethod
    async def id(FIO) -> int:
        query = t_dict_doctor.select(
            t_dict_doctor.c.doc_fio == FIO
        )
        res = await database.fetch_one(query)

        if res is not None:
            return res['doc_id']

        query = t_dict_doctor.insert().values(
            {
                "doc_fio": FIO,
                "date_update": datetime.now()
            }
        )
        await database.execute(query)

        query = t_dict_doctor.select(
            t_dict_doctor.c.doc_fio == FIO
        )
        res = await database.fetch_one(query)
        return res['doc_id']

    @staticmethod
    async def fio(ID) -> str:
        "Это не нужно, так как буду джойнить"
        query = t_dict_doctor.select(
            t_dict_doctor.c.doc_id == ID
        )
        res = await database.fetch_one(query)

        if res is not None:
            return res['doc_fio']
        return ''
