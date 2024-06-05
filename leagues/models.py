from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError

import uuid

from common.models import Event
from profiles.models import Profile

# Create your models here.
class League(Event):
    admins = models.ManyToManyField(Profile, related_name='league_admin')
    start_date = models.DateTimeField()


class LeagueSidepot(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league_sidepots')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    sidepot = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.league.name} -- {self.sidepot.name}'
    

class Roster(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league_rosters')
    date = models.DateField()

    def __str__(self):
        return f'{self.league.name} -- {self.date.strftime("%m/%d/%y")}'


class BowlerSidepotEntry(models.Model):
    bowler = models.ForeignKey('RosterEntry', on_delete=models.CASCADE)
    sidepot = models.ForeignKey(LeagueSidepot, on_delete=models.CASCADE)
    entry_count = models.PositiveIntegerField(default=1)

    def clean(self):
        if not self.sidepot.sidepot.allow_multiple_entries and self.entry_count > 1:
            raise ValidationError(f'Multiple entries are not allowed for {self.sidepot.name}')
        
    def __str__(self):
        return f'{self.bowler_entry.bowler} -- {self.sidepot.sidepot.name} x {self.entry_count}'
    

class RosterEntry(models.Model):
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='league_roster_entries')
    bowler = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='league_bowler')
    sidepots = models.ManyToManyField(LeagueSidepot, through=BowlerSidepotEntry, related_name='league_bowler_sidepot_entries')

    def __str__(self):
        return f'{self.league_roster.league.name} -- {self.league_roster.date.strftime("%m/%d/%y")} -- {self.bowler}'