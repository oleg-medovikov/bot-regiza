from pydantic import BaseModel
from datetime import datetime
from base import database, t_toxic_cases_errors, t_dict_doctor, \
    t_dict_mkb, t_dict_orgs
from sqlalchemy import select
from sqlalchemy.orm import aliased


class ToxicCaseError (BaseModel):
    case_biz_key:    int
    org_id:          int
    history_number:  str
    mkb_id:          int
    diagnoz_date:    datetime
    doc_smo:         int
    doc_md:          int
    error:           str

    async def add(self):
        # проверяем наличие по case_biz_key
        query = t_toxic_cases_errors.select(
            t_toxic_cases_errors.c.case_biz_key == self.case_biz_key
        )
        res = await database.fetch_one(query)

        if res is None:
            query = t_toxic_cases_errors\
                .insert().values(self.dict())
        else:
            query = t_toxic_cases_errors.update()\
                .where(
                    t_toxic_cases_errors.c.case_biz_key == self.case_biz_key
                    )\
                .values(self.dict())

        await database.execute(query)

    @staticmethod
    async def delete(CASE_BIZ_KEY: int):
        "удаляем ошибку если нормально загрузился в таблицу t_toxic_cases"
        query = t_toxic_cases_errors.delete().where(
            t_toxic_cases_errors.c.case_biz_key == CASE_BIZ_KEY
        )
        await database.execute(query)

    @staticmethod
    async def get_all(ORG: list) -> dict:
        t_doc_SMO = aliased(t_dict_doctor)
        t_doc_MD = aliased(t_dict_doctor)

        j = t_toxic_cases_errors.join(
            t_dict_orgs,
            t_toxic_cases_errors.c.org_id == t_dict_orgs.c.org_id
        ).join(
            t_dict_mkb,
            t_toxic_cases_errors.c.mkb_id == t_dict_mkb.c.mkb_id
        ).join(
            t_doc_SMO,
            t_toxic_cases_errors.c.doc_smo == t_doc_SMO.c.doc_id
        ).join(
            t_doc_MD,
            t_toxic_cases_errors.c.doc_md == t_doc_MD.c.doc_id
        )

        query = select([
            (t_toxic_cases_errors.c.case_biz_key).label('Идентификатор СМО'),
            (t_dict_orgs.c.org_name).label('Организация'),
            (t_toxic_cases_errors.c.history_number).label('Номер истории'),
            (t_dict_mkb.c.mkb_code).label('Диагноз'),
            (t_toxic_cases_errors.c.diagnoz_date).label('Дата отправки'),
            (t_doc_SMO.c.doc_fio).label('Врач СМО'),
            (t_doc_MD.c.doc_fio).label('Врач МД'),
            (t_toxic_cases_errors.c.error).label('Ошибка'),
        ]).select_from(j).where(
            t_toxic_cases_errors.c.org_id.in_(ORG)
        )

        res = await database.fetch_all(query)
        return [dict(r) for r in res]
