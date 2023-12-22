from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
def main(request):
    # notes = Note.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    return render(request, 'quotesapp/index.html')
