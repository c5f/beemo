from django.core.management.base import BaseCommand

from app.models import Call, Participant


def calculate_veg_servings_score(value):
    
    if value > 3:
        return 5

    elif value == 3:
        return 3

    elif value == 2:
        return 1

    else:
        return 0


def calculate_fruit_servings_score(value):
    
    if value > 2:
        return 5

    elif value == 2:
        return 3

    elif value == 1:
        return 1

    else:
        return 0


def calculate_fiber_grams_score(value):
    
    if value > 29:
        return 5

    elif value > 19:
        return 3

    elif value > 14:
        return 1

    else:
        return 0


def calculate_fat_grams_score(value, goal_value):
    
    percentage = value / goal_value

    if percentage < 1.1:
        return 5

    elif percentage < 1.2:
        return 3

    elif percentage < 1.4:
        return 1

    else:
        return 0


def calculate_steps_score(value, goal_value):
    
    difference = value - goal_value
    
    if difference < 1:
        return 5

    elif difference < 1001:
        return 3

    elif difference < 2001:
        return 1

    else:
        return 0


def update_adherence_score(participant, call):

    # Only calculate if all fields are present
    if (call.fat_grams and 
        call.fruit_servings and 
        call.fiber_grams and 
        call.veg_servings and 
        call.steps and 
        participant.base_fat_goal and 
        participant.base_step_goal):

        call.adherence_score = (
            calculate_veg_servings_score(call.veg_servings) +
            calculate_fruit_servings_score(call.fruit_servings) +
            calculate_fiber_grams_score(call.fiber_grams) +
            calculate_fat_grams_score(call.fat_grams, participant.base_fat_goal) +
            calculate_steps_score(call.steps, participant.base_step_goal)
        ) / 5.0

    else:
        call.adherence_score = None

    call.save()


def update_adherence_scores():
    
    for participant in Participant.objects.all():
        for call in participant.calls.all():
            update_adherence_score(participant, call)


class Command(BaseCommand):
    help = "Calculates and updates call adherence scores."

    def handle(self, *args, **options):
        
        update_adherence_scores()
