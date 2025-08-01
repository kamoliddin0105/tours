from modeltranslation.translator import register, TranslationOptions

from .models import TourDestination


@register(TourDestination)
class TourDestinationTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)
