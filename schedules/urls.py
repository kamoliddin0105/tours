from django.urls import path

from schedules.views import TourCalendarAPIView

urlpatterns = [
    path('tours/<int:tour_id>/calendar/', TourCalendarAPIView.as_view()),
]
