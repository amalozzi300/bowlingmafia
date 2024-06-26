# Generated by Django 5.0.6 on 2024-06-27 02:19

import django.core.validators
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BowlingCenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
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
            name='Bowler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handicap', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(300)])),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bowler', to='profiles.profile')),
            ],
        ),
    ]
