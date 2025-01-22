from django.urls import path
from .views import RegistrationView, LoginView, current_user_view

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', current_user_view, name='current_user'),

]
