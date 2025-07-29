from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.permisssions import IsAdminUserCustom
from accounts.serializers import UserSerializer
from tours.models import TourDestination, UserTour
from tours.serializers import TourDestinationSerializer, UserTourSerializer, CreateUserTourSerializer


class TourListCreateAPIView(CreateAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    permission_classes = [IsAdminUserCustom]


class TourRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = TourDestination.objects.all()
    serializer_class = TourDestinationSerializer
    permission_classes = [IsAdminUserCustom]


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


class BookTourAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateUserTourSerializer(data=request.data)
        if serializer.is_valid():
            tour = serializer.validated_data['tour']
            if UserTour.objects.filter(user=request.user, tour=tour).exists():
                return Response({"detail": "You already booked this tour."}, status=status.HTTP_400_BAD_REQUEST)

            UserTour.objects.create(user=request.user, tour=tour)
            return Response({"detail": "You booked this tour."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = UserTour.objects.filter(user=request.user)
        serializer = UserTourSerializer(bookings, many=True)
        return Response(serializer.data)


class CancelBookingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            booking = UserTour.objects.get(id=pk, user=request.user)
        except UserTour.DoesNotExist:
            return Response({"detail": "Tour not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == 'cancelled':
            return Response({"detail": "You already cancelled this tour."}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({"detail": "You cancelled this tour."}, status=status.HTTP_200_OK)


class ConfirmUserTourAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

    def post(self, request, pk):
        try:
            user_tour = UserTour.objects.get(pk=pk)

            if user_tour.status == 'Pending':
                user_tour.status = 'Confirmed'
                user_tour.save()
                return Response({'detail': 'Booking successfully confirmed.'}, status=status.HTTP_200_OK)

            elif user_tour.status == 'Confirmed':
                return Response({'detail': 'This booking is already confirmed.'}, status=status.HTTP_400_BAD_REQUEST)

            elif user_tour.status == 'Cancelled':
                return Response({'detail': 'This booking has already been cancelled. Cannot confirm.'},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({'detail': 'Invalid booking status.'}, status=status.HTTP_400_BAD_REQUEST)

        except UserTour.DoesNotExist:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
