from django.urls import path

from .views import (RegisterAPIView, LoginAPIView, MakeAdminApiView, RemoveAdminApiView, MakeTourManagerApiView,
                    RemoveTourManagerApiView, TourManagerListApiView, AddressAPIView,
    # ForgotPasswordAPIView,
    # ResetPasswordAPIView
                    )

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='auth_register'),
    path('login/', LoginAPIView.as_view(), name='auth_login'),
    # path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    # path('reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path('make/admin/<int:user_id>/', MakeAdminApiView.as_view(), name='make_admin'),
    path('remove/admin/<int:user_id>/', RemoveAdminApiView.as_view(), name='remove_admin'),

    path('tour-manager/', TourManagerListApiView.as_view(), name='tour_manager'),
    path('address/', AddressAPIView.as_view(), name='address'),

    path('make/tour_manager/<int:user_id>/', MakeTourManagerApiView.as_view(), name='make_tour_manager'),
    path('remove/tour_manager/<int:user_id>/', RemoveTourManagerApiView.as_view(), name='remove_tour_manager'),
]
