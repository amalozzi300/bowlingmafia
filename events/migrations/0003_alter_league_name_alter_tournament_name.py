# Generated by Django 5.0.6 on 2024-06-03 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_bowlingcenter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='name',
            field=models.CharField(default='NONE', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(default='NONE', max_length=256),
            preserve_default=False,
        ),
    ]