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
    sms_number = models.ForeignKey(Phone, blank=True, null=True, related_name='sms_participant')

    # Experiment Participant Fields
    base_fat_goal = models.PositiveIntegerField(blank=True, null=True)
    base_step_goal = models.PositiveIntegerField(blank=True, null=True)

    technology_touches = models.PositiveIntegerField(null=True)

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
