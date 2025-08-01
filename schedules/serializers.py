from rest_framework import serializers

from schedules.models import TourSchedule


class TourScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourSchedule
        fields = ['id', 'start_date', 'end_date', 'seats', 'seats']
