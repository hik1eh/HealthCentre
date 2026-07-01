from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from pacient.models import Pacient
from doctor.models import Doctor

from .forms import UserLoginForm, UserRegisterForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже вошли в аккаунт.')
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request, user)
                return redirect('/')
                if user_type == 'Doctor':
                    Doctor.objects.create(user=user, full_name=full_name)
                else:
                    Pacient.objects.create(user=user, full_name=full_name, email=email)
                messages.success(request, 'Account is created.')

    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, "authuser/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже вошли в аккаунт.')
        return redirect('/')

    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user_insctance = User.objects.get(email=email, is_active=True)
                user_authenticate = authenticate(request, email=email, password=password)

                if user_authenticate is not None:
                    login(request, user_authenticate)
                    messages.success(request, 'You are logged in.')
                    next_url = request.GET.get('next', '/')
                    return redirect(next_url)
                else:
                    messages.error(request, "Error. Login or password incorrect.")
            except:
                messages.error(request, "Haven't user with that email or password.")
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, "authuser/sign-in.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('/')
