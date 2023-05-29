from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, \
    DateTime, Boolean, Date, BigInteger

t_toxic_cases_errors = Table(
    "toxic_cases_errors",
    metadata,
    # идентификатор случая лечения пациента
    Column('case_biz_key', BigInteger, primary_key=True),

    # идентификатор организации dict_orgs
    Column('org_id', SmallInteger),

    # номер истории болезни
    Column('history_number', String),

    # диагноз МКБ dict_mkb
    Column('mkb_id', SmallInteger),

    # дата установки диагноза
    Column('diagnoz_date', DateTime),

    # ФИО врача Случая медицинского лечения
    Column('doc_smo', SmallInteger),

    # ФИО врача медицинского документа
    Column('doc_md', SmallInteger),

    # описание ошибки
    Column('error', SmallInteger),
)
