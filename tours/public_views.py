import calendar
from collections import defaultdict

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.paginition import MonthlyCheapTourPagination
from tours.filters import TourDestinationFilter, SimilarTourFilter, TourDestinationAllFilter
from tours.models import TourDestination, UserTour
from tours.serializers import TourDestinationSerializer, TourSerializer
from tours.swagger import hot_tours_schema, tour_calendar_schema, similar_tours_schema, grouped_tour_map_schema


class HotToursAPIView(APIView):
    @hot_tours_schema
    def get(self, request):
        hot_tours = TourDestination.objects.filter(is_featured=True).order_by('-created_at')
        serializer = TourDestinationSerializer(hot_tours, many=True)
        return Response(serializer.data)


class TourCalendarAPIView(APIView):
    @tour_calendar_schema
    def get(self, request):
        month_name = request.query_params.get('month')
        if not month_name:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            month_number = list(calendar.month_name).index(month_name.capitalize())
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = TourDestination.objects.filter(start_date__month=month_number).order_by('name', 'price_adult')

        seen = set()
        unique_cheapest = []
        for tour in queryset:
            if tour.name not in seen:
                unique_cheapest.append(tour)
                seen.add(tour.name)

        paginator = MonthlyCheapTourPagination()
        paginated = paginator.paginate_queryset(unique_cheapest, request)
        serializer = TourSerializer(paginated, many=True)

        return paginator.get_paginated_response(serializer.data)


class TourListFilterAPIView(ListAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourDestinationFilter


class SimilarTourFilterAPIView(ListAPIView):
    serializer_class = TourSerializer

    @similar_tours_schema
    def get_queryset(self):
        tour_id = self.kwargs['tour_id']
        tour_instance = get_object_or_404(TourDestination, id=tour_id)
        queryset = TourDestination.objects.exclude(id=tour_id)
        return SimilarTourFilter(
            data=self.request.GET,
            queryset=queryset,
            request=self.request,
            tour_instance=tour_instance
        ).qs


class TourListAPIView(ListAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer


class TourDetailAPIView(RetrieveAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    lookup_field = 'pk'


class GroupedTourMapAPIView(APIView):
    @grouped_tour_map_schema
    def get(self, request):
        data = defaultdict(list)
        tours = TourDestination.objects.filter(latitude__isnull=False, longitude__isnull=False)

        for tour in tours:
            region = tour.destination_country.region if tour.destination_country else None
            key = (region, tour.latitude, tour.longitude)
            data[key].append(tour)

        result = []
        for (region, lat, lon), tours_in_group in data.items():
            result.append({
                'region': region,
                'latitude': lat,
                'longitude': lon,
                'count': len(tours_in_group),
                'min_price': min(t.discount_price or t.price_adult for t in tours_in_group),
                'tours': [
                    {
                        'id': t.id,
                        'title': t.name,
                        'price': t.discount_price or t.price_adult
                    }
                    for t in tours_in_group
                ]
            })

        return Response(result)


class TourFilterAPIView(ListAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourDestinationAllFilter


class TourBookingAPIView(APIView):
    def post(self, request, pk):
        tour = get_object_or_404(TourDestination, pk=pk)

        booking = UserTour.objects.create(user=request.user, tour=tour)

        operator = tour.operator
        manager_info = None
        if operator and operator.user.role and operator.user.role.name == "TourManager":
            manager_info = {
                "full_name": f"{operator.user.first_name} {operator.user.last_name}",
                "phone_number": operator.phone_number,
                "telegram_link": f"https://t.me/{operator.telegram_username}" if operator.telegram_username else None,
            }

        return Response({
            "message": "Tour successfully booked",
            "tour": tour.name,
            "start_date": tour.start_date,
            "end_date": tour.end_date,
            "price": tour.price_adult,
            "manager": manager_info,
            "booking": booking,
        }, status=status.HTTP_201_CREATED)
