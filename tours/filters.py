from datetime import timedelta

import django_filters

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
