from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import StaticPage
from cms.serializers import StaticPageSerializer, StaticPageTranslatedSerializer


class StaticPageDetailAPIView(APIView):

    # permission_classes = (IsAuthenticated,)
    def get(self, request, slug):
        try:
            page = StaticPage.objects.get(slug=slug)
        except StaticPage.DoesNotExist:
            return Response({"detail": "Page not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StaticPageSerializer(page)
        return Response(serializer.data)

class StaticPageTranslatedAPIView(APIView):
    def get(self, request, slug):
        try:
            page = StaticPage.objects.get(slug=slug)
        except StaticPage.DoesNotExist:
            return Response({"detail": "Page not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StaticPageTranslatedSerializer(page, context={'request': request})
        return Response(serializer.data)
