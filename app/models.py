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


class Motor(models.Model):
    VEHICLE_CONDITION = [
        ('new', 'New'),
        ('excellent', 'Excellent'),
        ('very good', 'Very good'),
        ('good', 'Good'),
        ('smaller investments required', 'Smaller investments required'),
        ('not working', 'Not working')
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    made_at = models.IntegerField()
    milage = models.IntegerField()
    condition = models.CharField(max_length=50, choices=VEHICLE_CONDITION, default='new', blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="motorimages/")

    def __str__(self):
        return f' {self.year} {self.make} {self.model}'
