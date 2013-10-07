# Django
from django.core.management.base import BaseCommand

# Models
from sync.models import Session

from sync.models import RParticipant
from app.models import Participant


def update_participants(session):
    
    for rp in session.query(RParticipant).all():
        p = Participant(
            id=rp.id,
            coach=rp.coach
        )

        p.save()

    return session.query(RParticipant).count()


class Command(BaseCommand):
    help = "Updates beemo's database from remote database."

    def handle(self, *args, **options):
        session = Session()

        print 'Updating beemo participant database...'

        records = update_participants(session)

        print 'Finished updating beemo participant database for %d remote participants.' % records

        session.close()
