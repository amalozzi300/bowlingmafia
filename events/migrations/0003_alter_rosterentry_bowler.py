# Generated by Django 5.0.6 on 2024-07-11 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_bowling_centers'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rosterentry',
            name='bowler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster_entries', to='profiles.profile'),
        ),
    ]