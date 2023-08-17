from pydantic import BaseModel
from datetime import datetime, date
from base import database, t_toxic_cases, t_dict_doctor, \
    t_dict_mkb, t_dict_obser, t_dict_orgs
from sqlalchemy import desc, select, case, and_, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql import extract
from sqlalchemy import Integer
from sqlalchemy.sql.expression import false, true, cast

from pandas import DataFrame


class ToxicCase (BaseModel):
    case_biz_key:    int
    is_cancelled:    bool
    org_id:          int
    history_number:  str
    sex:             bool
    age:             int
    mkb_id:          int
    diadnoz_stage:   bool
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

    @staticmethod
    async def delete(CASE_BIZ_KEY):
        # просто удаляем строчку, так как case_biz_key отменен
        # устаревшая функция, я решил более не удалять
        query = t_toxic_cases.delete().where(
            t_toxic_cases.c.case_biz_key == int(CASE_BIZ_KEY)
        )

        await database.execute(query)

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
        t_2 = aliased(t_dict_obser)
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
            t_toxic_cases.c.org_id == t_dict_orgs.c.org_id,
            isouter=True
        ).join(
            t_dict_mkb,
            t_toxic_cases.c.mkb_id == t_dict_mkb.c.mkb_id,
            isouter=True
        ).join(
            t_doc_SMO,
            t_toxic_cases.c.doc_smo == t_doc_SMO.c.doc_id,
            isouter=True
        ).join(
            t_doc_MD,
            t_toxic_cases.c.doc_md == t_doc_MD.c.doc_id,
            isouter=True
        ).join(
            t_1101,
            and_(
                t_toxic_cases.c.o_1101 == t_1101.c.nsi_key,
                t_1101.c.obs_code == 1101),
            isouter=True
        ).join(
            t_2,
            and_(
                t_toxic_cases.c.age == cast(t_2.c.rpn_key, Integer),
                t_2.c.obs_code == 2),
            isouter=True
        ).join(
            t_1106,
            and_(
                t_toxic_cases.c.o_1106 == t_1106.c.nsi_key,
                t_1106.c.obs_code == 1106),
            isouter=True
        ).join(
            t_1108,
            and_(
                t_toxic_cases.c.o_1108 == t_1108.c.nsi_key,
                t_1108.c.obs_code == 1108),
            isouter=True
        ).join(
            t_1109,
            and_(
                t_toxic_cases.c.o_1109 == t_1109.c.nsi_key,
                t_1109.c.obs_code == 1109),
            isouter=True
        ).join(
            t_1110,
            and_(
                t_toxic_cases.c.o_1110 == t_1110.c.nsi_key,
                t_1110.c.obs_code == 1110),
            isouter=True
        ).join(
            t_1113,
            and_(
                t_toxic_cases.c.o_1113 == t_1113.c.nsi_key,
                t_1113.c.obs_code == 1113),
            isouter=True
        ).join(
            t_1115,
            and_(
                t_toxic_cases.c.o_1115 == t_1115.c.nsi_key,
                t_1115.c.obs_code == 1115),
            isouter=True
        ).join(
            t_1117,
            and_(
                t_toxic_cases.c.o_1117 == t_1117.c.nsi_key,
                t_1117.c.obs_code == 1117),
            isouter=True
        ).join(
            t_1119,
            and_(
                t_toxic_cases.c.o_1119 == t_1119.c.nsi_key,
                t_1119.c.obs_code == 1119),
            isouter=True
        ).join(
            t_1123,
            and_(
                t_toxic_cases.c.o_1123 == t_1123.c.nsi_key,
                t_1123.c.obs_code == 1123),
            isouter=True
        )

        query = select([
            (case(
                (and_(
                    t_toxic_cases.c.is_cancelled == false(),
                    t_toxic_cases.c.diadnoz_stage == true(),
                    t_1123.c.rpn_key.like('40%')
                ), 'Да'),
                else_='Нет'
                )).label('Попадает в выгрузку РПН'),
            (t_toxic_cases.c.o_303).label('Дата установления диагноза (303)'),
            (t_toxic_cases.c.case_biz_key).label('Идентификатор СМО'),
            (case(
                (t_toxic_cases.c.is_cancelled, 'отменен'),
                else_='актуальный',
            )).label('Статус СМО'),
            (t_dict_orgs.c.org_name).label('Организация'),
            (t_toxic_cases.c.history_number).label('Номер истории болезни'),
            (t_2.c.value).label('Возраст'),
            (case((t_toxic_cases.c.sex, 'М'), else_='Ж')).label('Пол'),
            (t_dict_mkb.c.mkb_code).label('Диагноз'),
            (case(
                (t_toxic_cases.c.diadnoz_stage, 'Заключительный'),
                else_='Другой',
            )).label('Этап установления диагноза'),
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
            (case(
                (t_toxic_cases.c.o_1112 == -1, None),
                else_=t_toxic_cases.c.o_1112,
            )).label('Время до смерти (1112)'),
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
            .select_from(j).where(and_(
                t_toxic_cases.c.o_303.between(START, END),
                t_toxic_cases.c.org_id.in_(MO)
            ))
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
            isouter=True
        ).join(
            t_dict_mkb,
            t_toxic_cases.c.mkb_id == t_dict_mkb.c.mkb_id,
            isouter=True
        ).join(
            t_1,
            and_(
                (extract('month', t_toxic_cases.c.o_303)) == t_1.c.nsi_key,
                t_1.c.obs_code == 1
            ),
            isouter=True
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

    @staticmethod
    async def search_history_number(NUMBER: str, ORG: list) -> dict:
        "поиск человека по истории болезни"
        t_1123 = aliased(t_dict_obser)
        t_1 = aliased(t_dict_obser)
        t_doc_SMO = aliased(t_dict_doctor)
        t_doc_MD = aliased(t_dict_doctor)

        j = t_toxic_cases.join(
            t_1123,
            and_(
                t_toxic_cases.c.o_1123 == t_1123.c.nsi_key,
                t_1123.c.obs_code == 1123
            ),
            isouter=True
        ).join(
            t_dict_mkb,
            t_toxic_cases.c.mkb_id == t_dict_mkb.c.mkb_id
        ).join(
            t_1,
            and_(
                (extract('month', t_toxic_cases.c.o_303)) == t_1.c.nsi_key,
                t_1.c.obs_code == 1
            ),
            isouter=True
        ).join(
            t_doc_SMO,
            t_toxic_cases.c.doc_smo == t_doc_SMO.c.doc_id,
            isouter=True
        ).join(
            t_doc_MD,
            t_toxic_cases.c.doc_md == t_doc_MD.c.doc_id,
            isouter=True
        ).join(
            t_dict_orgs,
            t_toxic_cases.c.org_id == t_dict_orgs.c.org_id,
            isouter=True
        )

        query = select([
            (t_1.c.value).label('Месяц'),
            (t_toxic_cases.c.history_number).label('История болезни'),
            (t_dict_orgs.c.org_name).label('Организация'),
            (t_toxic_cases.c.case_biz_key).label('case_biz_key'),
            (t_toxic_cases.c.is_cancelled).label('Помечен, как отмененный'),
            (t_toxic_cases.c.o_303).label('Дата установления диагноза (303)'),
            (t_1123.c.value).label('Район'),
            (t_dict_mkb.c.mkb_code).label('Диагноз'),
            (t_doc_SMO.c.doc_fio).label('Врач СМО'),
            (t_doc_MD.c.doc_fio).label('Врач МД'),
            (t_toxic_cases.c.errors).label('Ошибки заполнения'),
        ]).select_from(j).where(and_(
            t_toxic_cases.c.org_id.in_(ORG),
            t_toxic_cases.c.history_number == NUMBER
        ))
        res = await database.fetch_all(query)
        return [dict(r) for r in res]

    @staticmethod
    async def stat_cases_count():
        "Сводный отчет по количеству случаев по месяцам"
        t_1 = aliased(t_dict_obser)
        t_1123 = aliased(t_dict_obser)

        j = t_toxic_cases.join(
            t_1,
            and_(
                (extract('month', t_toxic_cases.c.o_303)) == t_1.c.nsi_key,
                t_1.c.obs_code == 1
            ),
            isouter=True
        ).join(
            t_dict_orgs,
            t_toxic_cases.c.org_id == t_dict_orgs.c.org_id,
            isouter=True
        ).join(
            t_1123,
            and_(
                t_toxic_cases.c.o_1123 == t_1123.c.nsi_key,
                t_1123.c.obs_code == 1123
                ),
            isouter=True
        )

        query = select([
            (t_1.c.nsi_key).label('index'),
            (t_1.c.value).label('Месяц 303'),
            (t_dict_orgs.c.org_name).label('Организация'),
            func.count(t_1.c.value).label('Количество случаев'),
            func.sum(
                case(
                    (t_toxic_cases.c.is_cancelled, func.cast(1, Integer)),
                    else_=func.cast(0, Integer)
                )
            ).label('Помечен как отмененный'),
            func.sum(
                case(
                    (t_toxic_cases.c.is_cancelled, func.cast(0, Integer)),
                    (t_toxic_cases.c.diadnoz_stage, func.cast(0, Integer)),
                    else_=func.cast(1, Integer)
                )
            ).label('Этап диагноза не заключительный'),
            func.sum(
                case(
                    (and_(
                        t_toxic_cases.c.is_cancelled == false(),
                        t_toxic_cases.c.diadnoz_stage
                    ), func.cast(1, Integer)),
                    else_=func.cast(0, Integer)
                )
            ).label('Актуальные случаи'),
            func.sum(
                case(
                    (and_(
                        t_toxic_cases.c.is_cancelled == false(),
                        t_toxic_cases.c.diadnoz_stage == true(),
                        t_1123.c.rpn_key.like('40%')
                    ), func.cast(1, Integer)),
                    else_=func.cast(0, Integer)
                )
                ).label('Попадает в выгрузку РПН'),
        ]).group_by(
            t_1.c.nsi_key,
            t_1.c.value,
            t_dict_orgs.c.org_name
        ).select_from(j).where(
            extract('year', t_toxic_cases.c.o_303) == datetime.now().year
        )

        res = await database.fetch_all(query)
        df = DataFrame(data=[dict(r) for r in res])
        del df['index']
        return df

    @staticmethod
    async def file_cases_xml(START: str, END: str) -> list:
        "вытаскиваем данные для РПН, импорт в программу"
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
            t_toxic_cases.c.org_id == t_dict_orgs.c.org_id,
            isouter=True
        ).join(
            t_dict_mkb,
            t_toxic_cases.c.mkb_id == t_dict_mkb.c.mkb_id,
            isouter=True
        ).join(
            t_1101,
            and_(
                t_toxic_cases.c.o_1101 == t_1101.c.nsi_key,
                t_1101.c.obs_code == 1101),
            isouter=True
        ).join(
            t_1106,
            and_(
                t_toxic_cases.c.o_1106 == t_1106.c.nsi_key,
                t_1106.c.obs_code == 1106),
            isouter=True
        ).join(
            t_1108,
            and_(
                t_toxic_cases.c.o_1108 == t_1108.c.nsi_key,
                t_1108.c.obs_code == 1108),
            isouter=True
        ).join(
            t_1109,
            and_(
                t_toxic_cases.c.o_1109 == t_1109.c.nsi_key,
                t_1109.c.obs_code == 1109),
            isouter=True
        ).join(
            t_1110,
            and_(
                t_toxic_cases.c.o_1110 == t_1110.c.nsi_key,
                t_1110.c.obs_code == 1110),
            isouter=True
        ).join(
            t_1113,
            and_(
                t_toxic_cases.c.o_1113 == t_1113.c.nsi_key,
                t_1113.c.obs_code == 1113),
            isouter=True
        ).join(
            t_1115,
            and_(
                t_toxic_cases.c.o_1115 == t_1115.c.nsi_key,
                t_1115.c.obs_code == 1115),
            isouter=True
        ).join(
            t_1117,
            and_(
                t_toxic_cases.c.o_1117 == t_1117.c.nsi_key,
                t_1117.c.obs_code == 1117),
            isouter=True
        ).join(
            t_1119,
            and_(
                t_toxic_cases.c.o_1119 == t_1119.c.nsi_key,
                t_1119.c.obs_code == 1119),
            isouter=True
        ).join(
            t_1123,
            and_(
                t_toxic_cases.c.o_1123 == t_1123.c.nsi_key,
                t_1123.c.obs_code == 1123),
            isouter=True
        )

        query = select([
            t_toxic_cases.c.o_303,
            t_toxic_cases.c.case_biz_key,
            t_dict_orgs.c.org_name,
            t_toxic_cases.c.history_number,
            t_toxic_cases.c.age,
            (case((t_toxic_cases.c.sex, '100'), else_='200')).label('sex'),
            t_dict_mkb.c.mkb_rpn,
            t_toxic_cases.c.diagnoz_date,  # лишнее?
            (t_1101.c.rpn_key).label('o_1101'),
            t_toxic_cases.c.o_1102,
            t_toxic_cases.c.o_1103,
            t_toxic_cases.c.o_1104,
            t_toxic_cases.c.o_1105,
            (t_1106.c.rpn_key).label('o_1106'),
            t_toxic_cases.c.o_1107,
            (t_1108.c.rpn_key).label('o_1108'),
            (t_1109.c.rpn_key).label('o_1109'),
            (t_1110.c.rpn_key).label('o_1110'),
            t_toxic_cases.c.o_1111,
            (case(
                (t_toxic_cases.c.o_1112 == -1, None),
                else_=t_toxic_cases.c.o_1112,
            )).label('o_1112'),
            (t_1113.c.rpn_key).label('o_1113'),
            (case(
                (t_toxic_cases.c.o_1114 < 0, None),
                else_=t_toxic_cases.c.o_1114
            )).label('o_1114'),
            (t_1115.c.rpn_key).label('o_1115'),
            t_toxic_cases.c.o_1116,
            (t_1117.c.rpn_key).label('o_1117'),
            t_toxic_cases.c.o_1118,
            (t_1119.c.rpn_key).label('o_1119'),
            (t_1123.c.rpn_key).label('o_1123'),
        ]).order_by(desc(t_toxic_cases.c.o_303))\
            .select_from(j).where(and_(
                t_toxic_cases.c.o_303.between(START, END),
                t_toxic_cases.c.is_cancelled == false(),
                t_toxic_cases.c.diadnoz_stage == true(),
                t_1123.c.rpn_key.like('40%')
            ))
        res = await database.fetch_all(query)
        return [dict(r) for r in res]
