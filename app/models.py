from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    username = models.CharField(unique=True, max_length=20)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    location = models.CharField(max_length=255, blank=True, null=True)
    favorite_ads = models.ManyToManyField('Advertisement', related_name='favorited_by', blank=True)

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

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='motors')
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    made_at = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year)]
    )
    mileage = models.PositiveIntegerField()
    condition = models.CharField(max_length=30, choices=VEHICLE_CONDITION, default='new', blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="motorimages/")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.name})"

    class Meta:
        ordering = ['brand', 'model']
        verbose_name = 'Motor'
        verbose_name_plural = 'Motors'

class Advertisement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='advertisements')
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, related_name='advertisements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title or 'Advertisement'} by {self.user.username} for {self.motor}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Advertisement'
        verbose_name_plural = 'Advertisements'


