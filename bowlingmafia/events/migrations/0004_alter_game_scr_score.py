# Generated by Django 5.0.6 on 2024-08-26 01:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0003_alter_game_scr_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='scr_score',
            field=models.PositiveIntegerField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(300)],
            ),
        ),
    ]
