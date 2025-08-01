from django.urls import path

from cms.views import StaticPageDetailAPIView, StaticPageTranslatedAPIView

urlpatterns = [
    path('<slug:slug>/', StaticPageDetailAPIView.as_view(), name='static-page'),
    path('translated/<slug:slug>/', StaticPageTranslatedAPIView.as_view(), name='static-page-translated'),
]
