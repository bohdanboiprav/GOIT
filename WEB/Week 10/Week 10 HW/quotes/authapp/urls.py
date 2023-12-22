from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = "authapp"

urlpatterns = [
    path('signup/', views.signupuser, name='signup'),
    # path('signin/',
    #      LoginView.as_view(template_name='authapp/login.html', form_class=LoginForm, redirect_authenticated_user=True),
    #      name='signin'),
    # path('logout/', LogoutView.as_view(template_name='authapp/logout.html'), name='logout')
]