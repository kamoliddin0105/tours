from django.urls import path

from tours.public_views import (
    TourListAPIView,
    TourDetailAPIView,
    MyToursAPIView,
    TourListFilterAPIView
)
from tours.views import (
    TourListCreateAPIView,
    TourRetrieveUpdateDestroyAPIView,
    AllUsersAPIView,
    BlockUserAPIView,
)

urlpatterns = [
    path('', TourListAPIView.as_view(), name='tour_list'),
    path('<int:id>/', TourDetailAPIView.as_view(), name='tour_detail'),
    path('my-tours/', MyToursAPIView.as_view(), name='my_tours'),
    path('filter/', TourListFilterAPIView.as_view(), name='tour_filter'),

    # admin
    path('admin/tours/', TourListCreateAPIView.as_view(), name='admin_tour_list_create'),
    path('admin/<int:pk>/', TourRetrieveUpdateDestroyAPIView.as_view(), name='admin_tour_detail'),
    path('admin/users/', AllUsersAPIView.as_view(), name='admin_all_users'),
    path('admin/users/<int:user_id>/block/', BlockUserAPIView.as_view(), name='admin_block_user'),

]
