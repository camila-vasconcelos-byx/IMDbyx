from django import forms 
from IMDbyx.models import CustomUser


class CustomUserForm(forms.Form):
    name = forms.CharField(max_length=150, required=True, label='name')
    email = forms.EmailField(required=True, label='email')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='senha')

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An user with this email already exists.')
        
        return email
    
    def save(self):
        data = self.cleaned_data

        user = CustomUser.objects.create_user(
            name = data['name'],
            email = data['email'],
            password = data['password']
        )

        user.is_superuser = False
        user.is_staff = False
        user.save()
        
        return user
