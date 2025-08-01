from modeltranslation.translator import register, TranslationOptions

from contact.models import ContactRequest


@register(ContactRequest)
class ContactRequestTranslationOptions(TranslationOptions):
    fields = ('message',)
