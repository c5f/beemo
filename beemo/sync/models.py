import datetime
import locale

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.models import Email
from app.models import Phone
from app.models import InterventionParticipant
from app.models import Call
from app.models import InterventionParticipantProblem

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# SQLAlchemy declarative base boilerplate
engine = create_engine('mysql://liveslocal:liveslocal123@localhost/liveslocal')

Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)


class RNode(Base):

    __tablename__ = 'node'
    __table_args__ = ({'autoload': False})

    nid = Column('nid', Integer, primary_key=True)
    created = Column('created', DateTime)
    n_type = Column('type', String)
    status = Column('status', Integer)


class RParticipant(Base):

    __tablename__ = 'content_type_participant'
    __table_args__ = ({'autoload': False})

    vid = Column('vid', Integer, primary_key=True)
    nid = Column('nid', Integer)
    pid = Column('field_participantid_value', String)
    ptype = Column('field_type_value', String)
    fat_grams = Column('field_fat_goal_value', String)
    steps = Column('field_step_goal_value', String)
    mobile = Column('field_sms_number_value', String)
    email = Column('field_email_email', String)


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


# Model utility functions
class RequiredValueError(Exception):
    """ Exception raised for required fields with no value.

        Attributes:
            field -- input field in which the error occurred
            msg -- explanation of the error
    """

    def __init__(self, field):
        self.field = field
        self.msg = 'Value: blank or \'-\''


def update_participants(session, issue_list):
    """ This method updates participant data within beemo by calling two helper
        methods which update control and intervention participant data.

        Keyword Arguments:
        session -- the SQLAlchemy session to be used to query data.
        issue_list -- a list of potential problems with remote participant
            data.
    """

    update_intervention_participants(session, issue_list)

    # TODO: Implement this method and uncomment this line.
    # update_control_participants(session, issue_list)


def update_intervention_participants(session, issue_list):

    for r_participant in session.query(
            RParticipant).filter_by(ptype=1):

        mobile = None

        if r_participant.mobile:
            mobile = Phone.objects.get_or_create(
                number=r_participant.mobile)[0]

        r_node = session.query(RNode).get(r_participant.nid)

        try:
            participant = InterventionParticipant.objects.get(
                pid=r_participant.pid)
        except InterventionParticipant.DoesNotExist:
            participant = InterventionParticipant(pid=r_participant.pid)

        participant.creation_date = datetime.datetime.fromtimestamp(
            r_node.created)
        participant.sms_number = mobile

        try:
            participant.base_fat_goal = massage_number(
                'base_fat_goal', r_participant.fat_grams)
        except (AttributeError, RequiredValueError):
            participant.base_fat_goal = None
        except ValueError:
            issue_list.append({
                'participant': participant.pid,
                'call_num': 'Error in participant object',
                'reason': 'Value: %s' % r_participant.fat_grams,
                'field': 'InterventionParticipant: Fat Goal'
            })

            participant.base_fat_goal = None

        try:
            participant.base_step_goal = massage_number(
                'base_step_goal', r_participant.steps)
        except (AttributeError, RequiredValueError):
            participant.base_step_goal = None
        except ValueError:
            issue_list.append({
                'participant': participant.pid,
                'call_num': 'Error in participant object',
                'reason': 'Value: %s' % r_participant.steps,
                'field': 'InterventionParticipant: Step Goal'
            })

            participant.base_step_goal = None

        if mobile:
            participant.phone_numbers.add(mobile)

        participant.save()

        if r_participant.email:
            email = Email.objects.get_or_create(
                email=r_participant.email.strip(), participant=participant)[0]


def update_phone_numbers(session, issue_list):

    # Get a list of the intervention group's node ids
    nids = [int(i) for (i,) in session.query(
        RParticipant.nid).filter_by(ptype=1)]

    for r_phone in session.query(RPhone).filter(RPhone.nid.in_(nids)):

        # Find the InterventionParticipant object for this phone number
        pid = session.query(RParticipant).filter_by(
            nid=r_phone.nid).first().pid
        participant = InterventionParticipant.objects.get(pid=pid)

        # Strip non-digit characters
        phone_number = ''.join([i for i in r_phone.phone if i.isdigit()])

        # Trim anything beyond 10 digits
        phone_number = phone_number[:10]

        # Add this phone number to our database
        phone = Phone.objects.get_or_create(number=phone_number)[0]

        # Add this phone number to this participant
        participant.phone_numbers.add(phone)


def update_emails(issue_list):

    with open('emails.txt', 'r') as email_list:

        for line in email_list:

            parts = str.split(line, ':')

            if len(parts) == 2:

                try:
                    participant = InterventionParticipant.objects.get(
                        pid=parts[0])

                    Email.objects.get_or_create(
                        email=parts[1].strip(), participant=participant)
                except InterventionParticipant.DoesNotExist:

                    issue_list.append({
                        'participant': parts[0],
                        'call_num': 'Error in email list',
                        'reason': 'Invalid InterventionParticipant ID in \
                            email list',
                        'field': 'participant id'
                    })


def massage_number(fieldname, input_string):

    if input_string is None or input_string == '-':
        raise RequiredValueError(fieldname)

    if '-' in input_string:
        strings = str.split(input_string, '-')

        assert len(strings) == 2, 'input string %s \
            is improperly formatted.' % input_string

        # Average the values if a range was provided
        return int(round((float(strings[0]) + float(strings[1])) / 2.0))

    elif '.' in input_string:

        # Round value if float was provided
        return int(round(float(input_string)))

    else:

        # Looks like the input string was clean
        return locale.atoi(input_string)


def update_calls(session, issue_list):

    # Get a list of the intervention group's node ids
    nids = [int(i) for (i,) in session.query(
        RParticipant.nid).filter_by(ptype=1)]

    # We are only concerned with completed calls that belong to our sample
    # group
    for r_call in session.query(RCall).filter(RCall.pnid.in_(nids)).filter(
            RCall.completed is not None):

        # Find the InterventionParticipant object for this call
        pid = session.query(RParticipant).filter_by(
            nid=r_call.pnid).first().pid
        participant = InterventionParticipant.objects.get(pid=pid)

        # Check if this Call object is already in our database
        try:
            call = Call.objects.get(
                participant=participant, number=r_call.number)
        except Call.DoesNotExist:
            call = Call(participant=participant, number=r_call.number)

        # Update fields
        call.completed_date = datetime.datetime.strptime(
            r_call.completed, '%Y-%m-%dT%H:%M:%S').date()

        if r_call.goal_met:
            call.goal_met = True

        try:
            call.veg_servings = massage_number(
                'veg_servings', r_call.veg_servings)
        except ValueError as ve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Vegetable Servings',
                'reason': 'Value: %s' % r_call.veg_servings
            })

            call.veg_servings = 0
        except RequiredValueError as rve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Vegetable Servings',
                'reason': rve.msg
            })

            call.veg_servings = 0

        try:
            call.fruit_servings = massage_number(
                'fruit_servings', r_call.fruit_servings)
        except ValueError as ve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Fruit Servings',
                'reason': 'Value: %s' % r_call.fruit_servings
            })

            call.fruit_servings = 0
        except RequiredValueError as rve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Fruit Servings',
                'reason': rve.msg
            })

            call.fruit_servings = 0

        try:
            call.fiber_grams = massage_number(
                'fiber_grams', r_call.fiber_grams)
        except ValueError as ve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Fiber Grams',
                'reason': 'Value: %s' % r_call.fiber_grams
            })

            call.fiber_grams = 0
        except RequiredValueError as rve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Fiber Grams',
                'reason': rve.msg
            })

            call.fiber_grams = 0

        try:
            call.fat_grams = massage_number('fat_grams', r_call.fat_grams)
        except ValueError as ve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Fat Grams',
                'reason': 'Value: %s' % r_call.fat_grams
            })

            call.fat_grams = 0
        except RequiredValueError as rve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Fat Grams',
                'reason': rve.msg
            })

            call.fat_grams = 0

        try:
            call.steps = massage_number('steps', r_call.steps)
        except ValueError as ve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Steps',
                'reason': 'Value: %s' % r_call.steps
            })

            call.steps = 0
        except RequiredValueError as rve:
            issue_list.append({
                'participant': participant.pid,
                'call_num': int(r_call.number),
                'field': 'Call: Steps',
                'reason': rve.msg
            })

            call.steps = 0

        call.save()


def update_problems(session, issue_list):

    # Get a list of the intervention group's node ids
    nids = [int(i) for (i,) in session.query(
        RParticipant.nid).filter_by(ptype=1)]

    for r_problem in session.query(RProblem).filter(
            RProblem.participant_nid.in_(nids)):

        # Find the InterventionParticipant for this problem
        pid = session.query(RParticipant).filter_by(
            nid=r_problem.participant_nid).first().pid
        participant = InterventionParticipant.objects.get(pid=pid)

        r_date = datetime.datetime.strptime(
            r_problem.date, '%Y-%m-%dT%H:%M:%S').date()

        # Check for an existing problem
        try:
            problem = InterventionParticipantProblem.objects.get(
                participant=participant, date=r_date)
        except InterventionParticipantProblem.DoesNotExist:
            problem = InterventionParticipantProblem(
                participant=participant, date=r_date)

        # Update field
        problem.problem = r_problem.problem_type

        problem.save()
