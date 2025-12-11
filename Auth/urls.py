from django.contrib.auth.views import PasswordResetDoneView

from Auth.views import RegisterView, LogoutView, LoginView, PasswordResetRequestView, PasswordResetVerifyView
from django.urls import path, include
from Auth.views import LogoutAllView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout_all'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/verify/', PasswordResetVerifyView.as_view(), name='password_reset_verify'),
]