from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = "authapp"

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),
]