from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, \
    DateTime, Boolean, Date, BigInteger, Integer

t_toxic_cases = Table(
    "toxic_cases",
    metadata,
    # идентификатор случая лечения пациента
    Column('case_biz_key', BigInteger, primary_key=True),

    # статус идентификатора, был ли он оменен
    Column('is_cancelled', Boolean),

    # идентификатор организации dict_orgs
    Column('org_id', SmallInteger),

    # номер истории болезни
    Column('history_number', String),

    # пол пациента
    Column('sex', Boolean),

    # возраст пациента RPN код
    Column('age', Integer),

    # диагноз МКБ dict_mkb
    Column('mkb_id', SmallInteger),

    # дата установки диагноза
    Column('diagnoz_date', DateTime),

    # ФИО врача Случая медицинского лечения
    Column('doc_smo', SmallInteger),

    # ФИО врача медицинского документа
    Column('doc_md', SmallInteger),

    # 303 - Дата установления диагноза
    Column('o_303', Date),

    # 1101 - Место происшествия код из справочника
    Column('o_1101', SmallInteger),

    # 1102 - Адрес места происшествия
    Column('o_1102', String),

    # 1103 - Наименование места происшествия
    Column('o_1103', String),

    # 1104 - Дата отравления
    Column('o_1104', Date),

    # 1105 - Дата первичного обращения
    Column('o_1105', Date),

    # 1106 - Токсичные вещества, часто встречающиеся
    Column('o_1106', Integer),

    # 1107 - Токсичные вещества
    Column('o_1107', String),

    # 1108 - Сочетание с алкоголем dict_boolean_alc?
    Column('o_1108', SmallInteger),

    # 1109 - Лицо, установившее диагноз
    Column('o_1109', SmallInteger),

    # 1110 - Оказана медицинская помощь
    Column('o_1110', SmallInteger),

    # 1111 - Место наступления смерти
    Column('o_1111', String),

    # 1112 - Время прошедшее от поступления в лпу до смерти в часах
    Column('o_1112', SmallInteger),

    # 1113 - Характер отравления
    Column('o_1113', SmallInteger),

    # 1114 - Количество отравившихся
    Column('o_1114', SmallInteger),

    # 1115 - Обстоятельства отравления
    Column('o_1115', SmallInteger),

    # 1116 - Обстоятельства отравления текст
    Column('o_1116', String),

    # 1117 - Место приобретения яда
    Column('o_1117', SmallInteger),

    # 1118 - Место приобретения яда текст
    Column('o_1118', String),

    # 1119 - Социальное положение
    Column('o_1119', SmallInteger),

    # 1123 - Район
    Column('o_1123', SmallInteger),

    # ошибки заполнения
    Column('errors', String),

)
