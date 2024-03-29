from .base import metadata

from sqlalchemy import Table, Column, BigInteger, SmallInteger, DateTime

t_logi = Table(
    "logi",
    metadata,
    Column('time',   DateTime),
    Column('u_id',   BigInteger),
    Column('action', SmallInteger),
)
