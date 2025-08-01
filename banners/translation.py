from modeltranslation.translator import register, TranslationOptions

from banners.models import Banner


@register(Banner)
class TourDestinationTranslationOptions(TranslationOptions):
    fields = ('title',)
