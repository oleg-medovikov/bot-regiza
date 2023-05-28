from pydantic import BaseModel
from datetime import datetime, date
from base import database, t_toxic_cases, t_dict_doctor, \
    t_dict_mkb, t_dict_obser, t_dict_orgs
from sqlalchemy import desc, select, case, and_, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql import extract

from pandas import DataFrame
from func import month_name


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
    o_303:           date
    o_1101:          int
    o_1102:          str
    o_1103:          str
    o_1104:          date
    o_1105:          date
    o_1106:          int
    o_1107:          str
    o_1108:          int
    o_1109:          int
    o_1110:          int
    o_1111:          str
    o_1112:          int
    o_1113:          int
    o_1114:          int
    o_1115:          int
    o_1116:          str
    o_1117:          int
    o_1118:          str
    o_1119:          int
    o_1123:          int
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
        ).join(
            t_1115,
            and_(
                t_toxic_cases.c.o_1115 == t_1115.c.nsi_key,
                t_1115.c.obs_code == 1115)
        ).join(
            t_1117,
            and_(
                t_toxic_cases.c.o_1117 == t_1117.c.nsi_key,
                t_1117.c.obs_code == 1117)
        ).join(
            t_1119,
            and_(
                t_toxic_cases.c.o_1119 == t_1119.c.nsi_key,
                t_1119.c.obs_code == 1119)
        ).join(
            t_1123,
            and_(
                t_toxic_cases.c.o_1123 == t_1123.c.nsi_key,
                t_1123.c.obs_code == 1123)
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
            (case(
                (t_toxic_cases.c.o_1114 < 0, None),
                else_=t_toxic_cases.c.o_1114
            )).label('Количество отравившихся (1114)'),
            (t_1115.c.value).label('Обстоятельства отравления (1115)'),
            (t_toxic_cases.c.o_1116).label('Обстоятельства текст (1116)'),
            (t_1117.c.value).label('Место приобретения яда (1117)'),
            (t_toxic_cases.c.o_1118).label('Место приобретения текст (1118)'),
            (t_1119.c.value).label('Социальное положение (1119)'),
            (t_1123.c.value).label('Район (1123)'),
            (t_toxic_cases.c.errors).label('Ошибки заполнения'),
            ]).order_by(desc(t_toxic_cases.c.o_303))\
            .select_from(j).where(
            t_toxic_cases.c.o_303.between(START, END)
        )
        if MO != 'all':
            query = query.where(
                t_toxic_cases.c.org_id == MO
            )
        res = await database.fetch_all(query)
        return [dict(r) for r in res]

    @staticmethod
    async def svod_toxic_district() -> list:
        t_1123 = aliased(t_dict_obser)
        t_1 = aliased(t_dict_obser)

        j = t_toxic_cases.join(
            t_1123,
            and_(
                t_toxic_cases.c.o_1123 == t_1123.c.nsi_key,
                t_1123.c.obs_code == 1123
            ),
        ).join(
            t_dict_mkb,
            t_toxic_cases.c.mkb_id == t_dict_mkb.c.mkb_id
        ).join(
            t_1,
            and_(
                (extract('month', t_toxic_cases.c.o_303)) == t_1.c.nsi_key,
                t_1.c.obs_code == 1
            ),
        )

        query = select([
            (t_toxic_cases.c.case_biz_key).label('id'),
            (t_1.c.value).label('Месяц'),
            (t_1.c.nsi_key).label('номер'),
            (t_1123.c.value).label('Район'),
            (t_dict_mkb.c.mkb_code).label('Диагноз'),
        ]).select_from(j).where(
            extract('year', t_toxic_cases.c.o_303) == datetime.now().year
        )

        res = await database.fetch_all(query)
        df = DataFrame(data=[dict(r) for r in res])

        df = df.pivot_table(
            index=['номер', 'Месяц', 'Район'],
            columns=['Диагноз'],
            values='id',
            aggfunc='count'
            )
        df = df.fillna('')

        return df







