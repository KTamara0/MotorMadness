# Generated by Django 5.2 on 2025-07-16 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='profile_image',
        ),
    ]
