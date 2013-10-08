from django.db import models


class Coach(models.Model):

    id      = models.IntegerField(primary_key=True)
    name    = models.CharField(max_length=60, unique=True)


class Clinic(models.Model):

    id      = models.IntegerField(primary_key=True)
    name    = models.CharField(max_length=255)

    # May need other details per study requirements.

class Participant(models.Model):

    id              = models.CharField(max_length=60, primary_key=True)
    coach           = models.ForeignKey('Coach', related_name='participants')
    clinic          = models.ForeignKey('Clinic', related_name='participants')
    creation_date   = models.DateTimeField()
    birthdate       = models.DateField()

    # Nutrition and fitness goals
    fat_goal        = models.TextField()
    fruit_goal        = models.TextField()
    veg_goal        = models.TextField()
    fiber_goal        = models.TextField()
    step_goal        = models.TextField()

    # Non-compliance Reason for reporting
    nc_reason       = models.TextField(blank=True)


class Call(models.Model):

    id              = models.IntegerField(primary_key=True)
    participant     = models.ForeignKey('Participant', related_name='calls')
    coach           = models.ForeignKey('Coach', related_name='calls')
    scheduled_date  = models.DateTimeField()
    completed_date  = models.DateTimeField()

    # Nutrition and fitness goals
    fat_goal        = models.TextField()
    fruit_goal        = models.TextField()
    veg_goal        = models.TextField()
    fiber_goal        = models.TextField()
    step_goal        = models.TextField()

    call_note       = models.TextField(blank=True)


class ParticipantNote(models.Model):

    id          = models.IntegerField(primary_key=True)
    participant = models.ForeignKey('Participant', related_name='p_notes')
    coach       = models.ForeignKey('Coach', related_name='p_notes')
    note        = models.TextField(blank=True)


class ParticipantProblem(models.Model):

    id          = models.IntegerField(primary_key=True)
    participant = models.ForeignKey('Participant', related_name='problems')
    problem     = models.TextField(blank=True)
