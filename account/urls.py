from django.urls import path
from .views import (SetNewPasswordSerializer, 
     RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView,student_register,register_view,
     login_view,complete_profile
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = "account"

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
    path('student_register/', student_register, name='student_register'),
    path('landlord_register/', student_register, name='landlord_register'),
    path('register/',register_view),
    path('login/',login_view),
    path('complete_profile/', complete_profile)
]
