# Generated by Django 5.0.6 on 2024-08-06 02:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                (
                    'event_ptr',
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to='events.event',
                    ),
                ),
                ('start_date', models.DateTimeField()),
                ('num_games', models.PositiveIntegerField(default=3)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('events.event',),
        ),
    ]
