from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='home'),
    path('author/<slug:auth_fullname>/', views.author, name='author'),
    path('add_author/', views.NewAuthor.as_view(), name='add_author'),
    path('add_quote/', views.NewQuote.as_view(), name='add_quote'),
]
