from rest_framework import serializers

from currency.models import Currency


class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'