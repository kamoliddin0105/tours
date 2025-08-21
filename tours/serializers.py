from rest_framework import serializers

from core.mixin import MultiLanguageSerializerMixin
from tours.models import TourDestination


class TourDestinationSerializer(serializers.ModelSerializer, MultiLanguageSerializerMixin):
    class Meta:
        model = TourDestination
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDestination
        fields = ['name', 'images']
