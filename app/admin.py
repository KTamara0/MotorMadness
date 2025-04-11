from django.contrib import admin
from .models import CustomUser, Motor, Advertisement

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Motor)
admin.site.register(Advertisement)