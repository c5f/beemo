from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, backref, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://liveslocal:liveslocal123@localhost/liveslocal')

# SQLAlchemy declarative base boilerplate
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)


class RNode(Base):

    __tablename__ = 'node'
    __table_args__ = ({'autoload': False})

    nid = Column('nid', Integer, primary_key=True)
    created = Column('created', DateTime)


class RParticipant(Base):

    __tablename__ = 'content_type_participant'
    __table_args__ = ({'autoload': False})

    vid = Column('vid', Integer, primary_key=True)
    nid = Column('nid', Integer)
    pid = Column('field_participantid_value', String)
    ptype = Column('field_type_value', Integer)
    fat_grams = Column('field_fat_goal_value', String)
    steps = Column('field_step_goal_value', String)
    mobile = Column('field_sms_number_value', String)


class RCall(Base):

    __tablename__ = 'content_type_call'
    __table_args__ = ({'autoload': False})

    vid = Column('vid', Integer, primary_key=True)
    number = Column('field_call_num_value', Integer)
    pnid = Column('field_participant_nid', Integer)
    completed = Column('field_date_completed_value', String)
    goal_met = Column('field_apply_prev_topic_value', String)
    veg_servings = Column('field_daily_veg_value', String)
    fruit_servings = Column('field_daily_fruit_value', String)
    fiber_grams = Column('field_daily_fiber_value', String)
    fat_grams = Column('field_daily_fat_value', String)
    steps = Column('field_daily_steps_value', String)


class RPhone(Base):

    __tablename__ = 'content_field_contact_phone'
    __table_args__ = ({'autoload': False})

    vid = Column('vid', Integer, primary_key=True)
    nid = Column('nid', Integer)
    delta = Column('delta', Integer)
    phone = Column('field_contact_phone_value', String)


class RProblem(Base):

    __tablename__ = 'content_type_participant_problem'
    __table_args__ = ({'autoload': False})

    vid = Column('vid', Integer, primary_key=True)
    date = Column('field_problem_date_value', DateTime)
    problem_type = Column('field_problem_type_value', String)
    participant_nid = Column('field_problem_part_nid', Integer)
