from rest_framework import serializers

from tours.models import TourDestination, UserTour


class TourDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDestination
        fields = '__all__'


class UserTourSerializer(serializers.ModelSerializer):
    tour = TourDestinationSerializer()

    class Meta:
        model = UserTour
        fields = '__all__'


