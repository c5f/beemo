from django.core.management.base import BaseCommand

from app.models import Participant


class Command(BaseCommand):
    help = "Updates technology touch counts using IMAPClient and Twilio's REST API."

    def handle(self, *args, **options):

        pass
