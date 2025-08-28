from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserIsTourManagerSerializer,
    TourAdminAddressSerializer, UserProfileSerializer
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

profile_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "first_name": openapi.Schema(type=openapi.TYPE_STRING),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING),
        "gmail": openapi.Schema(type=openapi.TYPE_STRING),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "username": openapi.Schema(type=openapi.TYPE_STRING),
    }
)

profile_update_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "first_name": openapi.Schema(type=openapi.TYPE_STRING),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING),
        "gmail": openapi.Schema(type=openapi.TYPE_STRING),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
        "password": openapi.Schema(type=openapi.TYPE_STRING),
    }
)

booking_create_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "tour_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Tour ID"),
    }
)

booking_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
        "tour": openapi.Schema(type=openapi.TYPE_STRING),
        "status": openapi.Schema(type=openapi.TYPE_STRING, enum=["pending", "confirmed", "canceled"]),
        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
    }
)

booking_list_response = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=booking_response
)
