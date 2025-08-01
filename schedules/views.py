from rest_framework.response import Response
from rest_framework.views import APIView

from schedules.models import TourSchedule
from schedules.serializers import TourScheduleSerializer


class TourCalendarAPIView(APIView):
    def get(self, request, tour_id):
        schedules = TourSchedule.objects.filter(tour_id=tour_id)
        serializer = TourScheduleSerializer(schedules, many=True)
        return Response(serializer.data)
    