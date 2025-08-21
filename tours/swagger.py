from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from .serializers import TourDestinationSerializer, TourSerializer

hot_tours_schema = swagger_auto_schema(
    operation_description="Is_featured=True bo'lgan tur paketlar ro'yxatini qaytaradi",
    responses={status.HTTP_200_OK: TourDestinationSerializer(many=True)},
)

tour_calendar_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            "month",
            openapi.IN_QUERY,
            description="Oy nomi (masalan: January, February...)",
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        status.HTTP_200_OK: TourSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: "Noto'g'ri oy nomi yoki kiritilmagan",
    },
)

tour_list_filter_schema = swagger_auto_schema(
    operation_description="region, duration, month bo‘yicha filterlash mumkin",
    responses={status.HTTP_200_OK: TourSerializer(many=True)},
)

similar_tours_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("tour_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="Asosiy tur IDsi"),
    ],
    responses={status.HTTP_200_OK: TourSerializer(many=True)},
)

tour_list_schema = swagger_auto_schema(
    responses={status.HTTP_200_OK: TourDestinationSerializer(many=True)},
)

tour_detail_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("pk", openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="Tur IDsi"),
    ],
    responses={status.HTTP_200_OK: TourDestinationSerializer()},
)

grouped_tour_map_schema = swagger_auto_schema(
    operation_description="Region, latitude, longitude bo‘yicha guruhlab qaytaradi",
    responses={status.HTTP_200_OK: "Guruhlangan tur ma'lumotlari"},
)

tour_create_list_schema = swagger_auto_schema(
    request_body=TourDestinationSerializer,
    responses={
        status.HTTP_201_CREATED: TourDestinationSerializer(),
        status.HTTP_200_OK: TourDestinationSerializer(many=True),
    },
)

tour_retrieve_update_destroy_schema = swagger_auto_schema(
    request_body=TourDestinationSerializer,
    responses={
        status.HTTP_200_OK: TourDestinationSerializer(),
        status.HTTP_204_NO_CONTENT: "O'chirildi",
    },
)

all_users_schema = swagger_auto_schema(
    responses={status.HTTP_200_OK: "Foydalanuvchilar ro'yxati"},
)

block_user_schema = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter("user_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER, description="Foydalanuvchi IDsi"),
    ],
    responses={
        status.HTTP_200_OK: "User blocked successfully",
        status.HTTP_404_NOT_FOUND: "User not found",
    },
)

region_price_schema = swagger_auto_schema(
    responses={status.HTTP_200_OK: "Har bir region uchun o'rtacha narx"},
)
