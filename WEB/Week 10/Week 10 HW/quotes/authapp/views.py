from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


# Create your views here.

def signupuser(request):
    # if request.user.is_authenticated:
    #     return redirect(to='quotesapp:main')
    #
    # if request.method == 'POST':
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(to='quotesapp:main')
    #     else:
    #         return render(request, 'authapp/signup.html', context={"form": form})

    return render(request, 'authapp/signup.html')
