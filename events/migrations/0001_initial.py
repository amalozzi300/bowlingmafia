# Generated by Django 5.0.6 on 2024-06-03 00:58

import localflavor.us.models
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0002_profile_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='BowlingCenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('street_address', models.CharField(max_length=128, verbose_name='address')),
                ('city', models.CharField(max_length=64)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('zip_code', localflavor.us.models.USZipCodeField(max_length=10)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(blank=True, max_length=128, null=True)),
                ('website', models.URLField(blank=True, max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('admins', models.ManyToManyField(related_name='league_admin', to='profiles.profile')),
                ('bowling_centers', models.ManyToManyField(related_name='%(class)s_bowling_center', to='events.bowlingcenter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('bowling_centers', models.ManyToManyField(related_name='%(class)s_bowling_center', to='events.bowlingcenter')),
                ('directors', models.ManyToManyField(related_name='tournament_director', to='profiles.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
