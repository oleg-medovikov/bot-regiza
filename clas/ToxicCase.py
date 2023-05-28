from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from base import database, t_toxic_cases, t_dict_doctor, \
    t_dict_mkb, t_dict_obser, t_dict_orgs
from sqlalchemy import desc, select, case, and_
from sqlalchemy.orm import aliased


class ToxicCase (BaseModel):
    case_biz_key:    int
    org_id:          int
    history_number:  str
    sex:             bool
    age:             int
    mkb_id:          int
    diagnoz_date:    datetime
    doc_smo:         int
    doc_md:          int
    o_303:           Optional[date]
    o_1101:          Optional[int]
    o_1102:          Optional[str]
    o_1103:          Optional[str]
    o_1104:          Optional[date]
    o_1105:          Optional[date]
    o_1106:          Optional[int]
    o_1107:          Optional[str]
    o_1108:          Optional[int]
    o_1109:          Optional[int]
    o_1110:          Optional[int]
    o_1111:          Optional[str]
    o_1112:          Optional[int]
    o_1113:          Optional[int]
    o_1114:          Optional[int]
    o_1115:          Optional[int]
    o_1116:          Optional[str]
    o_1117:          Optional[int]
    o_1118:          Optional[str]
    o_1119:          Optional[int]
    o_1123:          Optional[int]
    errors:          str

    async def add(self):
        # проверяем наличие по case_biz_key
        query = t_toxic_cases.select(
            t_toxic_cases.c.case_biz_key == self.case_biz_key
        )
        res = await database.fetch_one(query)

        if res is None:
            query = t_toxic_cases.insert().values(self.dict())
        else:
            query = t_toxic_cases.update()\
                .where(t_toxic_cases.c.case_biz_key == self.case_biz_key)\
                .values(self.dict())

        await database.execute(query)

    @staticmethod
    async def file_cases_mo(START: str, END: str, MO: int) -> list:
        "вытаскиваем данные для мед организаций, что они загрузили"
        t_doc_SMO = aliased(t_dict_doctor)
        t_doc_MD = aliased(t_dict_doctor)
        t_1101 = aliased(t_dict_obser)
        t_1106 = aliased(t_dict_obser)
        t_1108 = aliased(t_dict_obser)
        t_1109 = aliased(t_dict_obser)
        t_1110 = aliased(t_dict_obser)
        t_1113 = aliased(t_dict_obser)
        t_1115 = aliased(t_dict_obser)
        t_1117 = aliased(t_dict_obser)
        t_1119 = aliased(t_dict_obser)
        t_1123 = aliased(t_dict_obser)

        j = t_toxic_cases.join(
            t_dict_orgs,
            t_toxic_cases.c.org_id == t_dict_orgs.c.org_id
        ).join(
            t_dict_mkb,
            t_toxic_cases.c.mkb_id == t_dict_mkb.c.mkb_id
        ).join(
            t_doc_SMO,
            t_toxic_cases.c.doc_smo == t_doc_SMO.c.doc_id
        ).join(
            t_doc_MD,
            t_toxic_cases.c.doc_md == t_doc_MD.c.doc_id
        ).join(
            t_1101,
            and_(
                t_toxic_cases.c.o_1101 == t_1101.c.nsi_key,
                t_1101.c.obs_code == 1101)
        ).join(
            t_1106,
            and_(
                t_toxic_cases.c.o_1106 == t_1106.c.nsi_key,
                t_1106.c.obs_code == 1106)
        ).join(
            t_1108,
            and_(
                t_toxic_cases.c.o_1108 == t_1108.c.nsi_key,
                t_1108.c.obs_code == 1108)
        ).join(
            t_1109,
            and_(
                t_toxic_cases.c.o_1109 == t_1109.c.nsi_key,
                t_1109.c.obs_code == 1109)
        ).join(
            t_1110,
            and_(
                t_toxic_cases.c.o_1110 == t_1110.c.nsi_key,
                t_1110.c.obs_code == 1110)
        ).join(
            t_1113,
            and_(
                t_toxic_cases.c.o_1113 == t_1113.c.nsi_key,
                t_1113.c.obs_code == 1113)
        )


        query = select([
            (t_toxic_cases.c.o_303).label('Дата установления диагноза (303)'),
            (t_toxic_cases.c.case_biz_key).label('Идентификатор СМО'),
            (t_dict_orgs.c.org_name).label('Организация'),
            (t_toxic_cases.c.history_number).label('Номер истории болезни'),
            (t_toxic_cases.c.age).label('Возраст'),
            (case((t_toxic_cases.c.sex, 'М'), else_='Ж')).label('Пол'),
            (t_dict_mkb.c.mkb_code).label('Диагноз'),
            (t_doc_SMO.c.doc_fio).label('Врач СМО'),
            (t_doc_MD.c.doc_fio).label('Врач МД'),
            (t_toxic_cases.c.diagnoz_date).label('Дата отправки'),
            (t_1101.c.value).label('Место происшествия (1101)'),
            (t_toxic_cases.c.o_1102).label('Адрес места происшествия (1102)'),
            (t_toxic_cases.c.o_1103).label('Наименование мeста (1103)'),
            (t_toxic_cases.c.o_1104).label('Дата отравления (1104)'),
            (t_toxic_cases.c.o_1105).label('Дата первичного обращения (1105)'),
            (t_1106.c.value).label('Частые токсичные вещества (1106)'),
            (t_toxic_cases.c.o_1107).label('Токсичные вещества (1107)'),
            (t_1108.c.value).label('Сочетание с алкоголем (1108)'),
            (t_1109.c.value).label('Лицо, установившее диагноз (1109)'),
            (t_1110.c.value).label('Оказана медицинская помощь (1110)'),
            (t_toxic_cases.c.o_1111).label('Место наступления смерти (1111)'),
            (t_toxic_cases.c.o_1112).label('Время до смерти (1112)'),
            (t_1113.c.value).label('Характер отравления (1113)'),
            (t_toxic_cases.c.o_1114).label('Количество отравившихся (1114)'),


            ]).order_by(desc(t_toxic_cases.c.o_303))\
            .select_from(j).where(
            t_toxic_cases.c.o_303.between(START, END)
        )

        res = await database.fetch_all(query)
        return [dict(r) for r in res]








