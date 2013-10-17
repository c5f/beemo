from sqlalchemy import Column, String, Integer

from sync.models import Base


class RUser(Base):

    # Table configuration params
    __tablename__ = 'users'
    __table_args__ = ({'autoload': False})

    # Column defs (if any)
    uid     = Column('uid', Integer, primary_key=True)
    name    = Column('name', String, unique=True)
