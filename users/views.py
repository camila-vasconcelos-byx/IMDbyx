from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from django.http import JsonResponse
from IMDbyx.models import CustomUser
from .forms import CustomUserForm

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('list-movies')
        else:
            messages.success(request, ('There was an error logging in!'))
            return redirect('user-login')
    else:
        return render(request, 'users/login.html')

def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return user_login(request)
    
    else:
        form = CustomUserForm()
        
    return render(request, 'users/create_user.html', {
        'form': form
    })

def logout_user(request):
    logout(request)
    return redirect('list-movies')