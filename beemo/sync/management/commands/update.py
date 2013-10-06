from sync.models import Session

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Updates beemo's database from remote database."

    def handle(self, *args, **options):
        session = Session()

        print 'Got the session.'

        session.close()
