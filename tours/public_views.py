from collections import defaultdict

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from schedules.models import TourSchedule
from tours.filters import TourDestinationFilter
from tours.models import TourDestination, UserTour
from tours.serializers import TourDestinationSerializer, UserTourSerializer, TourMapSerializer


class TourListAPIView(ListAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer


class TourDetailAPIView(RetrieveAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    lookup_field = 'pk'


class MyToursAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_tours = UserTour.objects.filter(user=request.user)
        serializer = UserTourSerializer(user_tours, many=True)
        return Response(serializer.data)


class TourListFilterAPIView(ListAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourDestinationFilter


class TourCalendarAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, tour_id):
        schedules = TourSchedule.objects.filter(tour_id=tour_id).values('start_date', 'price')
        data = [
            {
                "date": s["start_date"],
                "price": s["price"],
            } for s in schedules
        ]
        return Response(data, status=status.HTTP_200_OK)


class TourMapAPIView(APIView):
    def get(self, request):
        tours = TourDestination.objects.filter(latitude__isnull=False, longitude__isnull=False)
        serializer = TourMapSerializer(tours, many=True)
        return Response(serializer.data)


class GroupedTourMapAPIView(APIView):
    def get(self, request):
        data = defaultdict(list)
        tours = TourDestination.objects.filter(latitude__isnull=False, longitude__isnull=False)

        for tour in tours:
            key = (tour.region, tour.latitude, tour.longitude)
            data[key].append(tour)

        result = []
        for (region, lat, lon), tours_in_group in data.items():
            result.append({
                'region': region,
                'latitude': lat,
                'longitude': lon,
                'count': len(tours_in_group),
                'min_price': min(t.price for t in tours_in_group),
                'tours': [
                    {
                        'id': t.id,
                        'title': t.title_uz,
                        'price': t.price
                    }
                    for t in tours_in_group
                ]
            })

        return Response(result)
