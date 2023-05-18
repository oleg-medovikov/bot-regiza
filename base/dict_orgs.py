from .base import metadata

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, SmallInteger, String, DateTime

t_dict_orgs = Table(
    "dict_orgs",
    metadata,
    Column('org_id', SmallInteger, primary_key=True),  # порядковый номер
    Column('org_biz_key', UUID),
    Column('org_name', String),
    Column('date_update', DateTime),
)
