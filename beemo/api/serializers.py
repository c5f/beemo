# Import models
from app.models import Call, Participant

from rest_framework import serializers

class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call


class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participant

"""
# Example serializers


class AssetSerializer(serializers.ModelSerializer):
    # campus = serializers.CharField(source='campus')
    # building = serializers.CharField(source='building')
    # room = serializers.CharField(source='room')
    # inventory_unit = serializers.CharField(source='inventory_unit')
    scans = ScanSerializer(many=True)
    campus = serializers.CharField(source='campus')
    building = serializers.CharField(source='building')
    room = serializers.CharField(source='room')
    department = serializers.CharField(source='department')
    scanned = serializers.SerializerMethodField('was_scanned')


    def was_scanned(self, asset):
        return Scan.objects.filter(asset=asset, scan_date__gt=asset.updated).count() > 0


    class Meta:
        model = Asset
"""
