# Generated by Django 5.0.6 on 2024-06-22 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0002_alter_tournament_bowling_centers'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
