from .base import metadata, database, engine
from .user import t_users
from .people import t_people

metadata.create_all(engine)

__all__ = [
    'metadata',
    'database',
    'engine',
    't_users',
    't_people',
    ]
