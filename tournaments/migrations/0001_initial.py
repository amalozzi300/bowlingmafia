# Generated by Django 5.0.6 on 2024-07-11 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='events.event')),
                ('num_qualifying_games', models.PositiveIntegerField(default=3)),
                ('directors', models.ManyToManyField(related_name='is_tournament_director', to='profiles.profile')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('events.event',),
        ),
    ]
