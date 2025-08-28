from datetime import timedelta

import django_filters
from django_filters.rest_framework import FilterSet, MultipleChoiceFilter, ChoiceFilter

from tours.models import TourDestination


class TourDestinationFilter(django_filters.FilterSet):
    start_point = django_filters.CharFilter(field_name='start_point__name', lookup_expr='icontains')
    location = django_filters.CharFilter(field_name='location__name', lookup_expr='icontains')

    min_nights = django_filters.NumberFilter(field_name='nights', lookup_expr='gte')
    max_nights = django_filters.NumberFilter(field_name='nights', lookup_expr='lte')

    hotel_star = django_filters.ChoiceFilter(
        field_name='hotel_star',
        choices=[(i, f"{i} stars") for i in range(1, 6)]
    )

    people_count = django_filters.NumberFilter(method='filter_people_count')
    start_date = django_filters.DateFilter(method='filter_by_start_date_range')

    class Meta:
        model = TourDestination
        fields = []

    def filter_people_count(self, queryset, name, value):
        return queryset.filter(
            adults__gte=value // 2,
            children__gte=value - (value // 2),
        )

    def filter_by_start_date_range(self, queryset, name, value):
        return queryset.filter(
            start_date__range=(value - timedelta(days=3), value + timedelta(days=3))
        )


class SimilarTourFilter(django_filters.FilterSet):
    class Meta:
        model = TourDestination
        fields = []

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, tour_instance=None):
        self.tour_instance = tour_instance
        super().__init__(data, queryset, request=request, prefix=prefix)

    def qs(self):
        if not self.tour_instance:
            return super().qs

        tour = self.tour_instance
        qs = self.queryset.exclude(id=tour.id)

        qs = qs.filter(
            location=tour.location,
            start_date__range=(tour.start_date - timedelta(days=3), tour.start_date + timedelta(days=3))
        )

        if tour.nights:
            qs = qs.filter(nights__range=(tour.nights - 2, tour.nights + 2))

        if tour.hotel_star:
            qs = qs.filter(hotel_star=tour.hotel_star)

        return qs

class TourDestinationAllFilter(FilterSet):
    # Checkbox orqali bir nechta qiymat yuborish mumkin
    hotel_rating = MultipleChoiceFilter(
        field_name="hotel_rating",
        choices=[(i, str(i)) for i in range(1, 11)],  # Masalan 1 dan 10 gacha
    )
    hotel_star = MultipleChoiceFilter(
        field_name="hotel_star",
        choices=[(i, f"{i} stars") for i in range(1, 6)],
    )
    beach_type = MultipleChoiceFilter(
        field_name="beach_type",
        choices=[("sand", "Qum"), ("pebble", "Tosh"), ("private", "Xususiy")],
    )
    meal_type = MultipleChoiceFilter(
        field_name="meal_type",
        choices=[
            ("BB", "Bed & Breakfast"),
            ("HB", "Half Board"),
            ("FB", "Full Board"),
            ("AI", "All Inclusive"),
        ],
    )
    is_hot = ChoiceFilter(field_name="is_hot")
    is_featured = ChoiceFilter(field_name="is_featured")

    class Meta:
        model = TourDestination
        fields = [
            "hotel_rating",
            "hotel_star",
            "beach_type",
            "meal_type",
            "is_hot",
            "is_featured",
        ]
