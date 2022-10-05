from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ConfirmEmailView,
    ConfirmPhoneView,
    ResetPasswordView,
    EditProfileView,
    ChangePasswordView,
)

app_name = 'Accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('utils/edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('utils/confirm-email/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('utils/confirm-phone/', ConfirmPhoneView.as_view(), name='confirm-phone'),
    path('utils/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('utils/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
]