from django.urls import path

from currency.views import CurrencyRateListAPIView, CurrencyRateUpdateAPIView

urlpatterns = [
    path('list/', CurrencyRateListAPIView.as_view(), name='currency-list'),
    path('update/<str:currency>/', CurrencyRateUpdateAPIView.as_view(), name='currency-update'),
]