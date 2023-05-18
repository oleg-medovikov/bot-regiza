from .base import metadata

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, SmallInteger, String, DateTime, Boolean, \
    Date

t_toxic_cases = Table(
    "toxic_cases",
    metadata,
    # идентификатор случая лечения пациента
    Column('case_biz_key', UUID, primary_key=True),

    # идентификатор организации
    Column('org_id', SmallInteger),

    # номер истории болезни
    Column('history_number', String),

    # пол пациента
    Column('sex', Boolean),

    # возраст пациента
    Column('age', SmallInteger),

    # диагноз МКБ
    Column('diagnoz', String),

    # дата установки диагноза
    Column('diagnoz_date', DateTime),

    # ФИО врача Случая медицинского лечения
    Column('doc_smo', String),

    # ФИО врача медицинского документа
    Column('doc_md', String),

    # 303 - Дата установления диагноза
    Column('303', Date),

    # 1101 - Место происшествия код из справочника
    Column('1101', SmallInteger),

    # 1102 - Адрес места происшествия
    Column('1102', String),

    # 1103 - Наименование места происшествия
    Column('1103', String),

    # 1104 - Дата отравления
    Column('1104', Date),

    # 1105 - Дата первичного обращения
    Column('1105', Date),

    # 1106 - Токсичные вещества, часто встречающиеся
    Column('1106', String),

    # 1107 - Токсичные вещества
    Column('1107', String),

    # 1108 - Сочетание с алкоголем
    Column('1108', SmallInteger),

    # 1109 - Лицо, установившее диагноз
    Column('1109', SmallInteger),

    # 1110 - Оказана медицинская помощь
    Column('1110', SmallInteger),

    # 1113 - Характер отравления
    Column('1113', SmallInteger),

    # 1114 - Количество отравившихся
    Column('1114', SmallInteger),

    # 1115 - Обстоятельства отравления
    Column('1115', SmallInteger),

    # 1116 - Обстоятельства отравления текст
    Column('1116', String),

    # 1117 - Место приобретения яда
    Column('1117', SmallInteger),

    # 1118 - Место приобретения яда текст
    Column('1118', String),

    # 1119 - Социальное положение
    Column('1119', SmallInteger),

    # 1123 - Район
    Column('1123', String),

    # ошибки заполнения
    Column('errors', String),

)



















