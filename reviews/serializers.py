from rest_framework import serializers

from core.mixin import MultiLanguageSerializerMixin
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer, MultiLanguageSerializerMixin):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user',)
