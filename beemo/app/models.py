from django.db import models


class Email(models.Model):

    email = models.EmailField(primary_key=True)
    participant = models.ForeignKey('Participant', related_name='emails')

    class Meta:
        app_label = 'app'
        verbose_name = 'Email Address'
        verbose_name_plural = 'Email Addresses'


class Phone(models.Model):

    number = models.CharField(max_length=10, primary_key=True)

    class Meta:
        app_label = 'app'
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'


class Participant(models.Model):

    pid = models.CharField(max_length=60, primary_key=True)
    creation_date = models.DateField()
    phone_numbers = models.ManyToManyField(Phone)
    sms_number = models.ForeignKey(
        Phone, blank=True, null=True, related_name='sms_participant')

    # Experiment Participant Fields
    base_fat_goal = models.PositiveIntegerField(blank=True, null=True)
    base_step_goal = models.PositiveIntegerField(blank=True, null=True)

    # Technology Touch Details
    emails_in = models.PositiveIntegerField(null=True, default=0)
    emails_out = models.PositiveIntegerField(null=True, default=0)

    calls_in = models.PositiveIntegerField(null=True, default=0)
    calls_out = models.PositiveIntegerField(null=True, default=0)

    sms_in = models.PositiveIntegerField(null=True, default=0)
    sms_out = models.PositiveIntegerField(null=True, default=0)

    @property
    def tt_in(self):
        return self.emails_in + self.calls_in + self.sms_in

    @property
    def tt_out(self):
        return self.emails_out + self.calls_out + self.sms_out

    @property
    def technology_touches(self):
        return self.tt_in + self.tt_out

    class Meta:
        app_label = 'app'
        verbose_name = u'Participant'
        verbose_name_plural = u'Participants'


class Call(models.Model):

    number = models.IntegerField()
    participant = models.ForeignKey(Participant, related_name='calls')
    completed_date = models.DateField()
    goal_met = models.BooleanField()

    veg_servings = models.PositiveIntegerField(null=True)
    fruit_servings = models.PositiveIntegerField(null=True)
    fiber_grams = models.PositiveIntegerField(null=True)
    fat_grams = models.PositiveIntegerField(null=True)
    steps = models.PositiveIntegerField(null=True)

    adherence_score = models.FloatField(null=True)

    class Meta:
        app_label = 'app'
        verbose_name = u'Call'
        verbose_name_plural = u'Calls'


class ParticipantProblem(models.Model):

    participant = models.ForeignKey('Participant')
    date = models.DateField()
    problem = models.TextField(blank=True)

    class Meta:
        app_label = 'app'
        verbose_name = u'Participant Problem'
        verbose_name_plural = u'Participant Problems'


# Model utility functions
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

    percentage = value / float(goal_value)

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


def calculate_adherence_score(participant, call):

    # Only calculate if all fields are present
    if (call.fat_grams and
            call.fruit_servings and
            call.fiber_grams and
            call.veg_servings and
            call.steps and
            participant.base_fat_goal and
            participant.base_step_goal):

        return (
            calculate_veg_servings_score(call.veg_servings) +
            calculate_fruit_servings_score(call.fruit_servings) +
            calculate_fiber_grams_score(call.fiber_grams) +
            calculate_fat_grams_score(
                call.fat_grams, participant.base_fat_goal) +
            calculate_steps_score(call.steps, participant.base_step_goal)
            ) / 5.0

    else:
        return None
