# Generated by Django 5.0.6 on 2024-06-18 06:32

import django.db.models.deletion
from django.db import migrations, models

from profiles.models import Profile


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0008_rename_game_leaguegame'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='owner',
            field=models.ForeignKey(default=Profile.objects.first().id, on_delete=django.db.models.deletion.CASCADE, related_name='owned_leagues', to='profiles.profile'),
            preserve_default=False,
        ),
    ]