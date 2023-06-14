from .base import metadata

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, BigInteger, String, DateTime

t_dict_orgs = Table(
    "dict_orgs",
    metadata,
    Column('time', DateTime),
    Column('u_id', BigInteger),  # порядковый номер
    Column('org_biz_key', UUID),
    Column('org_name', String),
    Column('date_update', DateTime),
)
