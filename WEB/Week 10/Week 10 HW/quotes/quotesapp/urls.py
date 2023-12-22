from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='home'),
    path('author/<int:auth_id>', views.author, name='author'),
]
