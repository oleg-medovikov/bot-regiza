from .base import metadata

from sqlalchemy import Table, Column, BigInteger, String, DateTime

t_users = Table(
    "users",
    metadata,
    Column('u_id', BigInteger),  # Идентификатор юзера в телеге
    Column('fio', String),  # ФИО юзера
    Column('org', String),  # Организация пользователя
    Column('role', String),  # профиль прав пользователя
    Column('date_create', DateTime),
    )
