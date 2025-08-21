from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserIsTourManagerSerializer,
    TourAdminAddressSerializer
)

register_schema = swagger_auto_schema(
    request_body=RegisterSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response("Muvaffaqiyatli ro'yxatdan o'tdi"),
        status.HTTP_400_BAD_REQUEST: "Xatolik yuz berdi",
    },
)

login_schema = swagger_auto_schema(
    request_body=LoginSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response("Login muvaffaqiyatli"),
        status.HTTP_400_BAD_REQUEST: "Telefon raqam yoki parol noto'g'ri",
    },
)

forgot_password_schema = swagger_auto_schema(
    request_body=ForgotPasswordSerializer,
    responses={status.HTTP_200_OK: "Kod yuborildi"},
)

reset_password_schema = swagger_auto_schema(
    request_body=ResetPasswordSerializer,
    responses={status.HTTP_200_OK: "Parol muvaffaqiyatli yangilandi"},
)

make_admin_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("user_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="Foydalanuvchi IDsi"),
    ],
    responses={
        status.HTTP_200_OK: "Admin qilindi"

    },
)

remove_admin_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("user_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="Foydalanuvchi IDsi"),
    ],
    responses={
        status.HTTP_200_OK: "Adminlik olib tashlandi",
    },
)

make_manager_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("user_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER),
    ],
    responses={status.HTTP_200_OK: "Tour Manager qilindi"},
)

remove_manager_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("user_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER),
    ],
    responses={status.HTTP_200_OK: "Tour Managerlik olib tashlandi"},
)

tour_manager_list_schema = swagger_auto_schema(
    responses={status.HTTP_200_OK: UserIsTourManagerSerializer(many=True)},
)

tour_admin_address_schema = swagger_auto_schema(
    responses={status.HTTP_200_OK: TourAdminAddressSerializer(many=True)},
)
