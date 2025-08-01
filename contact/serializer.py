from rest_framework import serializers

from contact.models import ContactRequest
from core.mixin import MultiLanguageSerializerMixin


class ContactRequestSerializer(serializers.ModelSerializer, MultiLanguageSerializerMixin):
    class Meta:
        model = ContactRequest
        fields = '__all__'