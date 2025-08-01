from django.urls import path

from contact.views import ContactMessageCreateAPIView

urlpatterns = [
    path('send/', ContactMessageCreateAPIView.as_view(), name='contact-send'),
]
