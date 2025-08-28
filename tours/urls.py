from django.urls import path

from tours.public_views import (
    TourListAPIView,
    TourDetailAPIView,
    TourListFilterAPIView, TourCalendarAPIView, GroupedTourMapAPIView, HotToursAPIView, SimilarTourFilterAPIView,
    TourFilterAPIView
)
from tours.views import (
    TourListCreateAPIView,
    TourRetrieveUpdateDestroyAPIView,
    AllUsersAPIView,
    BlockUserAPIView
)

urlpatterns = [
    # tours
    path('list/', TourListAPIView.as_view(), name='tour_list'),
    path('<int:id>/detail/', TourDetailAPIView.as_view(), name='tour_detail'),
    path('filter/', TourListFilterAPIView.as_view(), name='tour_filter'),
    path('<int:tour_id>/similar/', SimilarTourFilterAPIView.as_view(), name='similar-tours'),
    path('hot/', HotToursAPIView.as_view()),
    path('<int:tour_id>/calendar/', TourCalendarAPIView.as_view()),
    path('grouped-price-map/', GroupedTourMapAPIView.as_view(), name='grouped-price-map'),
    path('filter-all/', TourFilterAPIView.as_view(), name='tour_filter'),


    # admin
    path('admin/create/', TourListCreateAPIView.as_view(), name='admin_tour_list_create'),
    path('admin/<int:pk>/detail/', TourRetrieveUpdateDestroyAPIView.as_view(), name='admin_tour_detail'),
    path('admin/all-users/', AllUsersAPIView.as_view(), name='admin_all_users'),
    path('admin/users/<int:user_id>/block/', BlockUserAPIView.as_view(), name='admin_block_user'),
]
