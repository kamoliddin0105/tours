from modeltranslation.translator import register, TranslationOptions

from reviews.models import Review


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('text',)
