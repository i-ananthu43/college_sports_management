# Generated by Django 5.1.1 on 2024-11-01 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_corestudent_register_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='corestudent',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
