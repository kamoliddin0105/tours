from rest_framework import serializers

from core.mixin import MultiLanguageSerializerMixin
from tours.models import TourDestination, UserTour, TourPriceWatch


class TourDestinationSerializer(serializers.ModelSerializer, MultiLanguageSerializerMixin):
    class Meta:
        model = TourDestination
        fields = ['name', 'location', 'description', 'start_point', 'start_date', 'end_date', 'duration',
                  'price', 'price_children', 'discount_price', 'available_seats', 'is_featured', 'departure_dates',
                  'includes', 'images']
        write_only_fields = ['id', 'is_featured']


class UserTourSerializer(serializers.ModelSerializer):
    tour = TourDestinationSerializer()

    class Meta:
        model = UserTour
        fields = ['id', 'tour', 'status', 'has_attended', 'created_at']


class CreateUserTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTour
        fields = ['tour']


class TourPriceWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPriceWatch
        fields = '__all__'


class TourMapSerializer(serializers.ModelSerializer, MultiLanguageSerializerMixin):
    min_price = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = TourDestination
        fields = ['id', 'description', 'latitude', 'longitude', 'region', 'min_price', 'count']

    def get_min_price(self, obj):
        return obj.price

    def get_count(self, obj):
        return 1
