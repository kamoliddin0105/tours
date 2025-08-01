from rest_framework.generics import CreateAPIView

from contact.models import ContactRequest
from contact.serializer import ContactRequestSerializer


class ContactMessageCreateAPIView(CreateAPIView):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer
