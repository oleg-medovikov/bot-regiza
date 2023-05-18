from .base import metadata

from sqlalchemy import Table, Column, SmallInteger, String, DateTime

t_dict_mkb = Table(
    "dict_mkb",
    metadata,
    Column('mkb_id', SmallInteger, primary_key=True),  # порядковый номер
    Column('mkb_code', String),
    Column('mkb_rpn', String),
    Column('date_update', DateTime),
)
