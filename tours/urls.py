from django.urls import path

from tours.public_views import (
    TourListAPIView,
    TourDetailAPIView,
    MyToursAPIView,
    TourListFilterAPIView, TourCalendarAPIView, TourMapAPIView, GroupedTourMapAPIView
)
from tours.views import (
    TourListCreateAPIView,
    TourRetrieveUpdateDestroyAPIView,
    AllUsersAPIView,
    BlockUserAPIView, BookTourAPIView, MyBookingsAPIView, CancelBookingAPIView, ConfirmUserTourAPIView, HotToursAPIView,
    TourPriceWatchCreateAPIView,
)

urlpatterns = [
    # tours
    path('', TourListAPIView.as_view(), name='tour_list'),
    path('<int:id>/', TourDetailAPIView.as_view(), name='tour_detail'),
    path('my-tours/', MyToursAPIView.as_view(), name='my_tours'),
    path('filter/', TourListFilterAPIView.as_view(), name='tour_filter'),
    path('tours/hot/', HotToursAPIView.as_view()),
    path('price-watch/', TourPriceWatchCreateAPIView.as_view(), name='price-watch'),
    path('tours/<int:tour_id>/calendar/', TourCalendarAPIView.as_view()),
    path('price-map/', TourMapAPIView.as_view(), name='price-map'),
    path('grouped-price-map/', GroupedTourMapAPIView.as_view(), name='grouped-price-map'),

    # admin
    path('admin/tours/', TourListCreateAPIView.as_view(), name='admin_tour_list_create'),
    path('admin/<int:pk>/', TourRetrieveUpdateDestroyAPIView.as_view(), name='admin_tour_detail'),
    path('admin/users/', AllUsersAPIView.as_view(), name='admin_all_users'),
    path('admin/users/<int:user_id>/block/', BlockUserAPIView.as_view(), name='admin_block_user'),
    path('admin/confirm-booking/<int:pk>/', ConfirmUserTourAPIView.as_view(), name='confirm-booking'),

    # booking
    path('book/', BookTourAPIView.as_view(), name='tour_book'),
    path('my-bookings/', MyBookingsAPIView.as_view(), name='my_bookings'),
    path('book/<int:pk>/cancel/', CancelBookingAPIView.as_view(), name='cancel_booking'),

]
