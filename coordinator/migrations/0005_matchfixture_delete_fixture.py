# Generated by Django 5.1.1 on 2024-10-31 07:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_alter_sportevent_coordinator'),
        ('coordinator', '0004_fixture_delete_fixtureresult'),
        ('core', '0002_corestudent_register_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchFixture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField(default=1)),
                ('student_1_score', models.IntegerField(blank=True, null=True)),
                ('student_2_score', models.IntegerField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.sportevent')),
                ('student_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_student_1', to='core.corestudent')),
                ('student_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_student_2', to='core.corestudent')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='match_winner', to='core.corestudent')),
            ],
        ),
        migrations.DeleteModel(
            name='Fixture',
        ),
    ]
