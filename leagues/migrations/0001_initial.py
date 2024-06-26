# Generated by Django 5.0.6 on 2024-06-27 02:19

import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('is_archived', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField()),
                ('num_games', models.PositiveIntegerField(default=3)),
                ('admins', models.ManyToManyField(related_name='league_admin', to='profiles.profile')),
                ('bowling_centers', models.ManyToManyField(related_name='%(class)s_bowling_centers', to='common.bowlingcenter')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_leagues', to='profiles.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeagueSidepot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('HG', 'High Game'), ('HS', 'High Series'), ('WTA', 'Winner Takes All'), ('Elim', 'Eliminator'), ('MD', 'Mystery Doubles')], max_length=64)),
                ('entry_fee', models.DecimalField(decimal_places=2, max_digits=6)),
                ('payout_ratio', models.PositiveSmallIntegerField(default=6, validators=[django.core.validators.MinValueValidator(2)])),
                ('is_handicap', models.BooleanField(default=False)),
                ('games_used', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), blank=True, default=list, size=None)),
                ('is_reverse', models.BooleanField(blank=True, default=False)),
                ('allow_multiple_entries', models.BooleanField(default=False)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_sidepots', to='leagues.league')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BowlerSidepotEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_count', models.PositiveIntegerField(default=1)),
                ('sidepot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.leaguesidepot')),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('is_registration_open', models.BooleanField(default=True)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_rosters', to='leagues.league')),
            ],
        ),
        migrations.CreateModel(
            name='RosterEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bowler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_bowlers', to='common.bowler')),
                ('roster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_roster_entries', to='leagues.roster')),
                ('sidepots', models.ManyToManyField(through='leagues.BowlerSidepotEntry', to='leagues.leaguesidepot')),
            ],
        ),
        migrations.AddField(
            model_name='bowlersidepotentry',
            name='roster_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_bowler_sidepot_entries', to='leagues.rosterentry'),
        ),
        migrations.CreateModel(
            name='LeagueGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_number', models.PositiveIntegerField()),
                ('scr_score', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(300)])),
                ('hdcp_score', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(300)])),
                ('bowler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_bowler_scores', to='leagues.rosterentry')),
            ],
            options={
                'unique_together': {('bowler', 'game_number')},
            },
        ),
    ]
