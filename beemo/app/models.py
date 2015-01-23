from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Email(models.Model):

    email = models.EmailField(primary_key=True)

    # Generic foreign key relationship to Participant subclasses.
    participant_type = models.ForeignKey(ContentType)
    participant_pid = models.CharField(max_length=60)
    participant = generic.GenericForeignKey('participant_type',
                                            'participant_pid')

    class Meta:
        app_label = 'app'
        verbose_name = 'Email Address'
        verbose_name_plural = 'Email Addresses'


class Phone(models.Model):

    number = models.CharField(max_length=10, primary_key=True)

    # Generic foreign key relationship to Participant subclasses.
    participant_type = models.ForeignKey(ContentType)
    participant_pid = models.CharField(max_length=60)
    participant = generic.GenericForeignKey('participant_type',
                                            'participant_pid')

    class Meta:
        app_label = 'app'
        verbose_name = 'Phone Number'
        verbose_name_plural = 'Phone Numbers'


class Call(models.Model):

    number = models.IntegerField()
    completed_date = models.DateField()
    goal_met = models.BooleanField()

    veg_servings = models.PositiveIntegerField(null=True)
    fruit_servings = models.PositiveIntegerField(null=True)
    fiber_grams = models.PositiveIntegerField(null=True)
    fat_grams = models.PositiveIntegerField(null=True)
    steps = models.PositiveIntegerField(null=True)

    adherence_score = models.FloatField(null=True)

    # Generic foreign key relationship to Participant subclasses.
    participant_type = models.ForeignKey(ContentType)
    participant_pid = models.CharField(max_length=60)
    participant = generic.GenericForeignKey('participant_type',
                                            'participant_pid')

    class Meta:
        app_label = 'app'
        verbose_name = u'Call'
        verbose_name_plural = u'Calls'


class Participant(models.Model):
    """ The Participant model is an abstract superclass to each of the concrete
        ControlParticipant and InterventionParticipant models.

        It contains all of the information and behavior shared by both
        subclasses.
    """

    pid = models.CharField(max_length=60, primary_key=True)
    creation_date = models.DateField()
    sms_number = models.ForeignKey(Phone, null=True, blank=True,
                                   related_name='sms_%(class)s')

    # Reverse Generic Relationships
    phone_numbers = generic.GenericRelation(
        Phone, content_type_field='participant_type',
        object_id_field='participant_pid')

    emails = generic.GenericRelation(
        Email, content_type_field='participant_type',
        object_id_field='participant_pid')

    calls = generic.GenericRelation(
        Call, content_type_field='participant_type',
        object_id_field='participant_pid')

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
        abstract = True


class ControlParticipant(Participant):
    """ The ControlParticipant model does not contain any additional data to
        the fields provided by the Participant superclass.
    """

    class Meta(Participant.Meta):
        abstract = False
        app_label = 'app'
        verbose_name = 'Control Participant'
        verbose_name_plural = 'Control Participants'


class InterventionParticipant(Participant):
    """ The InterventionParticipant model stores the necessary information
        to calculate study adherence from base fat and step goal values.
    """

    base_fat_goal = models.PositiveIntegerField(blank=True, null=True)
    base_step_goal = models.PositiveIntegerField(blank=True, null=True)

    class Meta(Participant.Meta):
        abstract = False
        app_label = 'app'
        verbose_name = u'Intervention Participant'
        verbose_name_plural = u'Intervention Participants'


class ParticipantProblem(models.Model):

    date = models.DateField()
    problem = models.TextField(blank=True)

    # Generic foreign key relationship to Participant subclasses.
    participant_type = models.ForeignKey(ContentType)
    participant_pid = models.CharField(max_length=60)
    participant = generic.GenericForeignKey('participant_type',
                                            'participant_pid')

    class Meta:
        app_label = 'app'
        verbose_name = u'InterventionParticipant Problem'
        verbose_name_plural = u'InterventionParticipant Problems'


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


def calculate_adherence_score(i_part, call):
    """ This method calculates the adherence score using various techniques to
        glean whether a participant has been adhering to the nutrition and
        fitness requirements of the program.

        Keyword Arguments:
        i_part -- an InterventionParticipant instance with valid required
            nutrition and fitness information.
        call -- a Call instance with valid required nutrition and fitness
            information
    """

    # Only calculate if all fields are present
    if (call.fat_grams and
            call.fruit_servings and
            call.fiber_grams and
            call.veg_servings and
            call.steps and
            i_part.base_fat_goal and
            i_part.base_step_goal):

        return (
            calculate_veg_servings_score(call.veg_servings) +
            calculate_fruit_servings_score(call.fruit_servings) +
            calculate_fiber_grams_score(call.fiber_grams) +
            calculate_fat_grams_score(
                call.fat_grams, i_part.base_fat_goal) +
            calculate_steps_score(call.steps, i_part.base_step_goal)
            ) / 5.0

    else:
        return None
