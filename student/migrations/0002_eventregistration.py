# Generated by Django 5.1.1 on 2024-10-30 06:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_coordinatorassignedevent'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('house_name', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.sportevent')),
            ],
        ),
    ]
