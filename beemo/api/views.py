# Import Models
from app.models import Call
from app.models import InterventionParticipant

# Import Serializers
from api.serializers import CallSerializer
from api.serializers import InterventionParticipantSerializer

from rest_framework import generics
from rest_framework import filters

import django_filters


class CallList(generics.ListAPIView):
    serializer_class = CallSerializer

    filter_backends = (filters.OrderingFilter,)
    ordering = ['-completed_date']

    def get_queryset(self):
        return Call.objects.all()


class CallDetail(generics.RetrieveAPIView):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


class InterventionParticipantList(generics.ListAPIView):
    serializer_class = ParticipantSerializer

    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 500

    def get_queryset(self):
        return InterventionParticipant.objects.all()


class InterventionParticipantDetail(generics.RetrieveAPIView):
    queryset = InterventionParticipant.objects.all()
    serializer_class = InterventionParticipantSerializer
