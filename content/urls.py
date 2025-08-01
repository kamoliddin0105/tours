from django.urls import path

from content.views import ContentBlockAPIView

urlpatterns = [
    path('content/<str:key>/', ContentBlockAPIView.as_view()),
]
