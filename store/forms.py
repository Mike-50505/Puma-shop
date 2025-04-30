from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
class RegistroForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'email','placeholder': 'Correo electrónico'})
    )
    
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','placeholder': 'Confirmar contraseña'}),
        strip=False,
    )

    class Meta:
        model = CustomUser
        fields = ("email",)

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )