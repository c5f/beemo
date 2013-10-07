from django.db import models


class Participant(models.Model):

    id      = models.CharField(max_length=60, primary_key=True)
    coach   = models.IntegerField(blank=True, null=True)