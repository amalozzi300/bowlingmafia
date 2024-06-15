from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError

import uuid

from common.models import Bowler, Event, Game
from profiles.models import Profile
from sidepots.models import Sidepot

# Create your models here.
class League(Event):
    admins = models.ManyToManyField(Profile, related_name='league_admin')
    start_date = models.DateTimeField()
    num_games = models.PositiveIntegerField(default=3)


class LeagueSidepot(Sidepot):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league_sidepots')
    

class Roster(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league_rosters')
    date = models.DateField()

    def __str__(self):
        return f'{self.league.name} -- {self.date.strftime("%m/%d/%y")}'


class RosterEntry(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='league_roster_entries')
    bowler = models.ForeignKey(Bowler, on_delete=models.CASCADE, related_name='league_bowlers')
    sidepots = models.ManyToManyField(LeagueSidepot, through='BowlerSidepotEntry')

    def __str__(self):
        return f'{self.roster.league.name} -- {self.roster.date.strftime("%m/%d/%y")} -- {self.bowler}'


class BowlerSidepotEntry(models.Model):
    bowler = models.ForeignKey(RosterEntry, on_delete=models.CASCADE, related_name='league_bowler_sidepot_entries')
    sidepot = models.ForeignKey(LeagueSidepot, on_delete=models.CASCADE)
    entry_count = models.PositiveIntegerField(default=1)

    def clean(self):
        if not self.sidepot.allow_multiple_entries and self.entry_count > 1:
            raise ValidationError(f'Multiple entries are not allowed for {self.sidepot.type}')
        
    def __str__(self):
        return f'{self.bowler.bowler} -- {self.sidepot.type} x {self.entry_count}'
    

class LeagueGame(Game):
    bowler = models.ForeignKey(RosterEntry, on_delete=models.CASCADE, related_name='league_bowler_scores')

    class Meta:
        unique_together = ('bowler', 'game_number')