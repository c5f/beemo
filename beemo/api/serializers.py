# Import models
from app.models import Call
from app.models import Participant

from rest_framework import serializers

class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant
