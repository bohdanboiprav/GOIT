from django.urls import path
from . import views

app_name = 'authapp'

urlpatterns = [
    path('signup/', views.main, name='signup'),
    # path('login/', views.loginuser, name='login'),
    # path('logout/', views.logoutuser, name='logout'),
]