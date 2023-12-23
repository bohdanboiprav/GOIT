from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm

app_name = "authapp"

urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/',
         LoginView.as_view(template_name='authapp/login.html', form_class=LoginForm, redirect_authenticated_user=True,
                           next_page="quotesapp:home"),
         name='signin'),
    path('logout/', views.logoutuser, name='logout'),
]

# redirect='quotesapp:home'
# template_name='authapp/logout.html'
