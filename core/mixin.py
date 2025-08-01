class MultiLanguageSerializerMixin:
    def get_languages(self):
        request = self.context.get('request')
        if request:
            lang = request.headers.get('Accept-Language', 'uz').lower()
            return lang if lang in ['uz', 'ru', 'en'] else 'uz'
        return 'uz'

    def get_multilang_value(self, obj, field_base):
        lang = self.get_languages()
        return getattr(obj, f"{field_base}_{lang}", None)
