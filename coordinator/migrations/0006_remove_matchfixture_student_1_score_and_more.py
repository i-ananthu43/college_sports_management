# Generated by Django 5.1.1 on 2024-10-31 07:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator', '0005_matchfixture_delete_fixture'),
        ('core', '0002_corestudent_register_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchfixture',
            name='student_1_score',
        ),
        migrations.RemoveField(
            model_name='matchfixture',
            name='student_2_score',
        ),
        migrations.AddField(
            model_name='matchfixture',
            name='is_finalized',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='matchfixture',
            name='round_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='matchfixture',
            name='student_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student1_matches', to='core.corestudent'),
        ),
        migrations.AlterField(
            model_name='matchfixture',
            name='student_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student2_matches', to='core.corestudent'),
        ),
        migrations.AlterField(
            model_name='matchfixture',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.corestudent'),
        ),
    ]
