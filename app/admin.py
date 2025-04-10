from django.contrib import admin
from .models import CustomUser, Motor

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Motor)