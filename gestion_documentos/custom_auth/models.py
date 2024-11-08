from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El Email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("correo electrónico", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def tiene_2fa_configurado(self):
        return TOTPDevice.objects.filter(user=self, confirmed=True).exists()

    def desactivar_2fa(self):
        TOTPDevice.objects.filter(user=self).delete()
