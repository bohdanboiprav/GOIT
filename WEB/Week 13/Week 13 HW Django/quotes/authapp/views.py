from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


# Create your views here.
class RegisterView(View):
    template_name = 'authapp/signup.html'
    form_class = RegisterForm
    login_required = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotesapp:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаємо {username}. Ваш акаунт успішно створено")
            return redirect(to="authapp:signin")
        return render(request, self.template_name, {"form": form})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quotesapp:home')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authapp/password_reset.html'
    email_template_name = 'authapp/password_reset_email.html'
    html_email_template_name = 'authapp/password_reset_email.html'
    success_url = reverse_lazy('authapp:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'authapp/password_reset_subject.txt'
