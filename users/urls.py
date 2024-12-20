from django.urls import path
from . import views

urlpatterns = [
    path('login', views.user_login, name='user-login'),
    path('create-user', views.create_user, name='create-user')
]
