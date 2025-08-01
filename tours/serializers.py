from rest_framework import serializers

from tours.models import TourDestination, UserTour


class TourDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDestination
        fields = ['name', 'location', 'description', 'start_point', 'start_date', 'end_date', 'duration',
                  'price', 'price_children', 'discount_price', 'available_seats', 'is_featured', 'departure_dates',
                  'includes', 'images']
        write_only_fields = ['id','is_featured']


class UserTourSerializer(serializers.ModelSerializer):
    tour = TourDestinationSerializer()

    class Meta:
        model = UserTour
        fields = ['id', 'tour', 'status', 'has_attended', 'created_at']


class CreateUserTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTour
        fields = ['tour']
