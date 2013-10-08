from sqlalchemy import Column, String, Integer

from sync.models import Base


class RParticipant(Base):

    # Table configuration params
    __tablename__ = 'content_type_participant'
    __table_args__ = ({'autoload': False})

    # Column defs (if any)
    vid         = Column('vid', Integer, primary_key=True)
    nid         = Column('nid', Integer)
    id          = Column('field_participantid_value', String)
    coach_id    = Column('field_preferred_coach_uid', Integer)
    clinic_id   = Column('field_clinic_id_value', Integer)
    birthdate   = Column('field_dob_value', String)
    nc_reason   = Column('field_non_compliance_reason', String)

    # Nutrition goals
    fat_goal    = Column('field_fat_goal_value', String)
    fruit_goal  = Column('field_fruit_goal_value', String)
    veg_goal    = Column('field_veg_goal_value', String)
    fiber_goal  = Column('field_fiber_goal_value', String)
    step_goal   = Column('field_step_goal_value', String)
