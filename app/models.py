from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    location = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

