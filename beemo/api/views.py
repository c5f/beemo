from libfso.contrib.locus.models import Building, Room

# Import Models
from app.models import Call, Participant

# Import Serializers
from app.serializers import CallSerializer, ParticipantSerializer

from rest_framework import generics
from rest_framework import filters

import django_filters


class CallList(generics.ListAPIView):
    serializer_class = CallSerializer

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 150

    def get_queryset(self):
        return Call.objects.all()


class CallDetail(generics.RetrieveAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


class ParticipantList(generics.ListAPIView):
    serializer_class = ParticipantSerializer

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 150

    def get_queryset(self):
        return Participant.objects.all()


class ParticipantDetail(generics.RetrieveAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
