from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, UserDetailAPIView, SetNewPasswordSerializer, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = "account"

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user_detail"),
    path("register/", UserCreateAPIView.as_view(), name="user_create"),
    path("<int:id>/", UserDetailAPIView.as_view(), name="user_detail"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]
