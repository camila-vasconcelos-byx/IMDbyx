from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'birth_date')  # Adicione os campos que você criou

    # Se você quiser personalizar mais os campos, você pode adicionar validadores ou lógica de limpeza aqui