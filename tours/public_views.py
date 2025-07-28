from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tours.filters import TourDestinationFilter
from tours.models import TourDestination, UserTour
from tours.serializers import TourDestinationSerializer, UserTourSerializer


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
