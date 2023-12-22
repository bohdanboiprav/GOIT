from django.shortcuts import render, redirect
from django.views import View
from .models import Quote, Tag, Author


# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quotes": quotes})


def author(request, auth_id):
    # new_auth_name = auth_name.replace("-", " ")
    author_data = Author.objects.filter(pk=auth_id).first()
    return render(request, 'quotesapp/author.html', {"author": author_data})

