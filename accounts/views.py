import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.permisssions import IsAdminUserCustom
from accounts.serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer


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


RESET_TOKENS = {}


# class ForgotPasswordAPIView(APIView):
#     def post(self, request):
#         serializer = ForgotPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         value = serializer.validated_data['email_or_phone']
#
#         try:
#             user = User.objects.get(gmail=value) if "@" in value else User.objects.get(phone_number=value)
#         except User.DoesNotExist:
#             return Response({"error": "Foydalanuvchi topilmadi"}, status=404)
#
#         token = str(uuid.uuid4())
#         RESET_TOKENS[token] = {"user_id": user.id, "created": timezone.now()}
#
#         # E-mail orqali yuborish:
#         if user.gmail:
#             send_mail(
#                 subject="Parolni tiklash",
#                 message=f"Parolingizni tiklash uchun havola: {settings.BASE_URL}/reset-password?token={token}",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[user.gmail],
#             )
#
#         return Response({"detail": "Parolni tiklash uchun ko‘rsatmalar yuborildi"}, status=200)
#
#
# class ResetPasswordAPIView(APIView):
#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         token = serializer.validated_data['token']
#         new_password = serializer.validated_data['new_password']
#
#         data = RESET_TOKENS.get(token)
#         if not data:
#             return Response({"error": "Token noto‘g‘ri yoki eskirgan"}, status=400)
#
#         try:
#             user = User.objects.get(id=data['user_id'])
#             user.set_password(new_password)
#             user.save()
#             RESET_TOKENS.pop(token, None)
#             return Response({"detail": "Parol muvaffaqiyatli o‘zgartirildi"})
#         except User.DoesNotExist:
#             return Response({"error": "Foydalanuvchi topilmadi"}, status=404)


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
