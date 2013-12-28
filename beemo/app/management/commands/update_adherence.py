from django.core.management.base import BaseCommand

from app.models import Call, Participant, calculate_adherence_score


def update_adherence_scores():
    
    for participant in Participant.objects.all():
        for call in participant.calls.all():
            call.adherence_score = calculate_adherence_score(participant, call)
            call.save()


class Command(BaseCommand):
    help = "Calculates and updates call adherence scores."

    def handle(self, *args, **options):
        
        update_adherence_scores()
