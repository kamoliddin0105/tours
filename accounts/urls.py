from django.urls import path
from .views import RegisterAPIView, LoginAPIView, MakeAdminApiView, RemoveAdminApiView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth_register'),
    path('login/', LoginAPIView.as_view(), name='auth_login'),
    path('make/admin/<int:user_id>/', MakeAdminApiView.as_view(), name='make_admin'),
    path('remove/admin/<int:user_id>/', RemoveAdminApiView.as_view(), name='remove_admin')
]
