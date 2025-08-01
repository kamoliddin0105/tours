from django.urls import path

from reviews.views import ReviewListCreateAPIView

urlpatterns = [
    path('reveiw-list/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
]
