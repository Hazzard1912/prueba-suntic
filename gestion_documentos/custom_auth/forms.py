from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class VerificacionTOTPForm(forms.Form):
    codigo = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa el código de 6 dígitos",
            }
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class LoginForm(AuthenticationForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Contraseña"}
        ),
    )

