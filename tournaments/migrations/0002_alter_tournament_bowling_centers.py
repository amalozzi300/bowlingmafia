# Generated by Django 5.0.6 on 2024-06-05 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='bowling_centers',
            field=models.ManyToManyField(related_name='%(class)s_bowling_centers', to='common.bowlingcenter'),
        ),
    ]