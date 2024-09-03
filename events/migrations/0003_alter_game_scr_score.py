# Generated by Django 5.0.6 on 2024-08-24 02:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_alter_roster_slug_alter_sidepot_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='scr_score',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(300)]),
        ),
    ]
