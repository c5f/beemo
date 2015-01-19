from django.contrib import admin

from app import models


admin.site.register(models.Email)
admin.site.register(models.Phone)
admin.site.register(models.InterventionParticipant)
admin.site.register(models.ParticipantProblem)
admin.site.register(models.Call)
