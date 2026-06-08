# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("receptionist", "Receptionist"),
        ("customer", "Customer"),
        ("staff","Staff"),
    )

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    google_id = models.CharField(
    max_length=255,
    blank=True,
    null=True,
    unique=True
)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "admin"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
    
from django.db import models
from django.conf import settings


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.email