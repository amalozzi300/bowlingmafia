# Generated by Django 5.0.6 on 2024-06-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0011_alter_leaguesidepot_is_reverse'),
    ]

    operations = [
        migrations.AddField(
            model_name='roster',
            name='is_registration_open',
            field=models.BooleanField(default=True),
        ),
    ]