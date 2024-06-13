# Generated by Django 5.0.6 on 2024-06-05 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0003_alter_bowlersidepotentry_bowler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bowlersidepotentry',
            name='bowler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_bowler_sidepot_entries', to='leagues.rosterentry'),
        ),
        migrations.AlterField(
            model_name='game',
            name='bowler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='league_bowler_scores', to='leagues.rosterentry'),
        ),
        migrations.AlterField(
            model_name='rosterentry',
            name='sidepots',
            field=models.ManyToManyField(through='leagues.BowlerSidepotEntry', to='leagues.leaguesidepot'),
        ),
    ]