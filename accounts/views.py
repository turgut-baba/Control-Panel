from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Vendor
import Control_Panel.settings as sett
from enum import Enum, unique


@unique
class Auth(Enum):
    user = 0
    vendor = 1
    admin = 2
    developer = 3


def user_vendor(request: str) -> HttpResponse:
    vendor_users = Vendor.objects.filter(auth_level=1)
    context = {
        "vendors": vendor_users,
    }
    return render(request, 'registration/vendor.html', context)


def add_vendor(request: str) -> HttpResponse:
    pass
    return render(request, 'registration/add_vendor.html')


def register_view(request: str) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_user(request: str) -> HttpResponse:
    logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(name=username, password=password)
        if user is not None:
            if user.is_active:
                if 'remembered' in request.POST.getlist('remember'):
                    ...
                    #sett.SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
                login(request, user)
                return redirect('stock_control:index')
    return render(request, 'registration/login.html')


@login_required
def panel_settings(request: str) -> HttpResponse:
    return render(request, 'settings.html')


@login_required
def logout_user(request: str) -> HttpResponse:
    logout(request)
    return redirect('registration/login.html')
