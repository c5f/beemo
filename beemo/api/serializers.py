# Import models
from app.models import Call
from app.models import InterventionParticipant

from rest_framework import serializers

class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call


class InterventionParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterventionParticipant
