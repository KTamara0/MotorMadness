# Generated by Django 5.1.5 on 2025-04-11 13:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_motor_options_alter_motor_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='motor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='motors', to=settings.AUTH_USER_MODEL),
        ),
    ]
