from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("subscriptions:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Акаунт створено. Ласкаво просимо!")
            return redirect("subscriptions:dashboard")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})