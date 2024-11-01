# Generated by Django 5.1.1 on 2024-10-31 17:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_alter_sportevent_coordinator'),
        ('coordinator', '0007_matchfixture_student_1_score_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('first_prize', models.CharField(max_length=100)),
                ('second_prize', models.CharField(max_length=100)),
                ('third_prize', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('sport_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.sportevent')),
            ],
        ),
    ]