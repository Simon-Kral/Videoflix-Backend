from django.urls import path
from .views import RegistrationView, LoginView, current_user_view, activate_account, ForgotPasswordView, reset_password

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', current_user_view, name='current_user'),
    path('activate/<uidb64>/<token>', activate_account, name='activate_account'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>', reset_password, name='reset_password'),
]
