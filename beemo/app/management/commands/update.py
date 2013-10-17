import datetime

# Django
from django.core.management.base import BaseCommand

# Models
from sync.models import Session, RParticipant, RUser, RClinic
from app.models import Coach, Clinic, Participant, Call, ParticipantNote, ParticipantProblem


def update_coaches(session):
    
    for ruser in session.query(RUser).all():
        try:
            coach = Coach.objects.get(cid=ruser.uid)
        except Coach.DoesNotExist:
            coach = Coach(
                cid=ruser.uid
            )

        coach.name = ruser.name
        coach.save()

    return session.query(RUser).count()


def update_clinics(session):
    
    for rclinic in session.query(RClinic).all():
        try:
            clinic = Clinic.objects.get(vid=rclinic.vid)
        except Clinic.DoesNotExist:
            clinic = Clinic(
                vid=rclinic.vid
            )

        clinic.cid = rclinic.clinic_id
        clinic.name = rclinic.name
        clinic.save()


    return session.query(RClinic).count()


def update_participants(session):

    for rpart in session.query(RParticipant).filter_by(p_type=1):
        try:
            participant = Participant.objects.get(pid=rpart.pid)
        except Participant.DoesNotExist:
            participant = Participant(
                pid=rpart.pid
            )

        # Sync fields
        participant.creation_date = datetime.datetime.now().date() # From node table
        participant.birthdate = datetime.datetime.now().date() # FROM UNIX TIMESTAMP?!

        participant.fat_goal = rpart.fat_goal
        participant.fruit_goal = rpart.fruit_goal
        participant.veg_goal = rpart.veg_goal
        participant.fiber_goal = rpart.fiber_goal
        participant.step_goal = rpart.step_goal

        # Sync foreign key references
        try:
            participant.coach = Coach.objects.get(cid=rpart.coach_id)
        except Coach.DoesNotExist:
            participant.coach = None

        try:
            participant.clinic = Clinic.objects.get(vid=rpart.clinic_id)
        except Clinic.DoesNotExist:
            participant.clinic = None

        participant.save()
    
    return session.query(RParticipant).count()


class Command(BaseCommand):
    help = "Updates beemo's database from remote database."

    def handle(self, *args, **options):
        session = Session()

        print 'Updating beemo coach database...'

        count = update_coaches(session)

        print 'Finished updating beemo coach database for %d remote user objects.\n' % count

        print 'Updating beemo clinic database...'

        count = update_clinics(session)

        print 'Finished updating beemo clinic database for %d remote clinic objects.\n' % count

        print 'Updating beemo participant database...'

        count = update_participants(session)

        print 'Finished updating beemo participant database for %d remote participant objects.\n' % count

        session.close()
