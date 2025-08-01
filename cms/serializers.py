from rest_framework import serializers

from cms.models import StaticPage
from core.mixin import MultiLanguageSerializerMixin


class StaticPageSerializer(serializers.ModelSerializer, MultiLanguageSerializerMixin):
    class Meta:
        model = StaticPage
        fields = ['slug', 'title_uz', 'title_ru', 'title_en', 'content_uz', 'content_ru', 'content_en']

class StaticPageTranslatedSerializer(serializers.ModelSerializer, MultiLanguageSerializerMixin):
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = StaticPage
        fields = ['slug', 'title', 'content']

    def get_title(self, obj):
        return self.get_multilang_value(obj, 'title')

    def get_content(self, obj):
        return self.get_multilang_value(obj, 'content')
