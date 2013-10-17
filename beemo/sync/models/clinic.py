from sqlalchemy import Column, String, Integer

from sync.models import Base


class RClinic(Base):

    # Table configuration params
    __tablename__ = 'content_type_clinic'
    __table_args__ = ({'autoload': False})

    # Column defs (if any)
    vid         = Column('vid', Integer, primary_key=True)
    clinic_id   = Column('field_clinic_number_value', String, unique=True)
    name        = Column('field_clinic_name_value', String)
