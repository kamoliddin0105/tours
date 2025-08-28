from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.permisssions import IsAdminUserCustom, IsSuperUserUserCustom
from accounts.serializers import RegisterSerializer, LoginSerializer, UserIsTourManagerSerializer, \
    TourAdminAddressSerializer, UserProfileSerializer
from accounts.swagger import register_schema, login_schema, make_admin_schema, remove_admin_schema, make_manager_schema, \
    remove_manager_schema, tour_manager_list_schema, tour_admin_address_schema, booking_create_request, booking_response


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterAPIView(APIView):
    @register_schema
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            "msg": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.",
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    @login_schema
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        tokens = get_tokens_for_user(user)
        return Response({
            "msg": "Kirish muvaffaqiyatli amalga oshirildi.",
            "tokens": tokens
        }, status=status.HTTP_200_OK)


class MakeAdminApiView(APIView):
    permission_classes = [IsSuperUserUserCustom, ]

    @make_admin_schema
    def patch(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.is_admin = True
            user.save()
            return Response({"msg": f"{user.phone_number} admin qilindi."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)


class RemoveAdminApiView(APIView):
    permission_classes = [IsSuperUserUserCustom, ]

    @remove_admin_schema
    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_admin:
            return Response({"message": "Bu foydalanuvchi allaqachon admin emas"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_admin = False
        user.save()
        return Response({"message": "Foydalanuvchidan adminlik olib tashlandi"},
                        status=status.HTTP_200_OK)


class MakeTourManagerApiView(APIView):
    permission_classes = [IsAdminUserCustom, ]

    @make_manager_schema
    def patch(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.is_tour_manager = True
            user.save()
            return Response({"msg": f"{user.phone_number} tour manager qilindi."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)


class RemoveTourManagerApiView(APIView):
    permission_classes = [IsAdminUserCustom, ]

    @remove_manager_schema
    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_tour_manager:
            return Response({"message": "Bu foydalanuvchi allaqachon tour manager emas"},
                            status=status.HTTP_400_BAD_REQUEST)

        user.is_manager = False
        user.save()
        return Response({"message": "Foydalanuvchidan tour managerlik olib tashlandi"},
                        status=status.HTTP_200_OK)


class TourManagerListApiView(ListAPIView):
    queryset = User.objects.filter(is_tour_manager=True)
    serializer_class = UserIsTourManagerSerializer
    permission_classes = [IsAdminUserCustom, IsSuperUserUserCustom, ]


class AddressAPIView(APIView):
    queryset = User.objects.filter(is_admin=True)
    serializer_class = TourAdminAddressSerializer


class UserProfileAPIView(RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileUpdateAPIView(UpdateAPIView):
    serializer_class = UserProfileSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

