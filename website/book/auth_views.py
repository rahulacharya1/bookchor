from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, logout, login as auth_login

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        data = form.save(commit=False)
        data.set_password(password)
        data.save()
        return redirect('login')
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        
        login_user = authenticate(username=username, password=password)
        
        if login_user is not None:
            auth_login(request, login_user)
            return redirect('home')
        
        form.add_error(None, "Invalid Username or Password")
        
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
