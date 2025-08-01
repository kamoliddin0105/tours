from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import ContentBlock


class ContentBlockAPIView(APIView):
    def get(self, request, key):
        content = get_object_or_404(ContentBlock, key=key)
        return Response({
            'title': content.title,
            'body': content.body,
        })
