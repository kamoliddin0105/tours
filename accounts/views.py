from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.permisssions import IsAdminUserCustom
from accounts.serializers import RegisterSerializer, LoginSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterAPIView(APIView):
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
    permission_classes = [IsAdminUserCustom, ]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.is_admin = True
            user.save()
            return Response({"msg": f"{user.phone_number} admin qilindi."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi."}, status=status.HTTP_404_NOT_FOUND)


class RemoveAdminApiView(APIView):
    permission_classes = [IsAdminUserCustom, ]

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
