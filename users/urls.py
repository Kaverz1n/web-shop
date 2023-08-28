from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    RegisterView, EmailConfirmSentView, EmailConfirmedView, EmailFailedConfirmView,
    UserConfirmEmailView, PasswordResetSentView, get_new_password, UserProfileUpdateView
)

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='email_confirm'),
    path('sent_email/', EmailConfirmSentView.as_view(), name='sent_email'),
    path('confirmed_email/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('failed_confirm_email/', EmailFailedConfirmView.as_view(), name='email_failed_confirmed'),
    path('password_reset/', get_new_password, name='password_reset'),
    path('sent_password/', PasswordResetSentView.as_view(), name='sent_password'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile')
]
