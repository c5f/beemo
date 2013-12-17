from django.core.management.base import BaseCommand


def update_adherence_scores():
    pass


def update_touch_counts():
    pass


class Command(BaseCommand):
    help = "Calculates call adherence scores and participant technology touch counts."

    def handle(self, *args, **options):
        
        update_adherence_scores()
        update_touch_counts()
