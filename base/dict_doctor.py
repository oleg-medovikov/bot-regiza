from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, DateTime

t_dict_doctor = Table(
    "dict_doctor",
    metadata,
    Column('doc_id', SmallInteger, primary_key=True),  # порядковый номер
    Column('doc_fio', String),
    Column('date_update', DateTime),
)
