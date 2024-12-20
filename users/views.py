from django.shortcuts import render

# Create your views here.

def user_login(request):
    return render(request, 'users/login.html')

def create_user(request):
    return render(request, 'users/create_user.html')