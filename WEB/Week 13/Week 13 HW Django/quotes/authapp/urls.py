from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView

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

    path('reset-password/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='authapp/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='authapp/password_reset_confirm.html',
                                          success_url='/authapp/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='authapp/password_reset_complete.html'),
         name='password_reset_complete'),
]

# redirect='quotesapp:home'
# template_name='authapp/logout.html'
