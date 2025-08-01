import django_filters
from django.db.models import Q

from tours.models import TourDestination


class TourDestinationFilter(django_filters.FilterSet):
    region = django_filters.CharFilter(field_name='location', lookup_expr='iexact')
    duration = django_filters.ChoiceFilter(
        field_name='duration',
        choices=[('7_days', '7 kun'), ('14_days', '14 kun'), ('1_month', '1 oy')]
    )
    month = django_filters.NumberFilter(method='filter_by_month')
    is_hot = django_filters.BooleanFilter(field_name='is_hot')

    class Meta:
        model = TourDestination
        fields = ['region', 'duration', 'month', 'is_hot']

    def filter_by_month(self, queryset, name, value):
        return queryset.filter(
            Q(start_date__month=value) | Q(end_date__month=value)
        )
