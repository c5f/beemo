from sqlalchemy import Column, String, Integer

from sync.models import Base


class RParticipant(Base):

    # Table configuration params
    __tablename__ = 'content_type_participant'
    __table_args__ = ({'autoload': False})

    # Column defs (if any)
    vid     = Column('vid', Integer, primary_key=True)
    id      = Column('field_participantid_value', String)
    coach   = Column('field_preferred_coach_uid', Integer)
