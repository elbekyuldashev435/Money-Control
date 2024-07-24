from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Siz muvafaqqiyatli kirdingiz.')
            return redirect('get-home')
        else:
            messages.error(request, 'Username yoki Parol xato!!!.')

    return render(request, 'users/login.html')


def logout_user(request):
    logout(request.use)
    return redirect('login')


def signup_user(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if username and password1 and password2 and password1 == password2:
            if first_name and last_name:

                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )

                user.set_password(password1)
                user.save()
                login(request, user)

                return redirect('get-home')
    return render(request, 'users/signup.html')