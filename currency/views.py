from rest_framework.generics import ListAPIView, UpdateAPIView

from currency.models import Currency
from currency.serializers import CurrencyRateSerializer


class CurrencyRateListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyRateSerializer

class CurrencyRateUpdateAPIView(UpdateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyRateSerializer
    lookup_field = 'CURRENCY_CHOICES'