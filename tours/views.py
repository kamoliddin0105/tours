from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.permisssions import IsAdminUserCustom
from accounts.serializers import UserSerializer
from tours.models import TourDestination, UserTour
from tours.serializers import TourDestinationSerializer, UserTourSerializer


class TourListCreateAPIView(CreateAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    permission_classes = [IsAdminUserCustom]


class TourRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    permission_classes = [IsAdminUserCustom]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class AllUsersAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUserCustom]


class BlockUserAPIView(APIView):
    permission_classes = [IsAdminUserCustom]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
            return Response({"detail": "User blocked successfully."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
