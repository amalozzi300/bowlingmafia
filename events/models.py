from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

import uuid
from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField

from profiles.models import Profile
from sidepots.models import Sidepot

# Create your models here.
class BowlingCenter(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    street_address = models.CharField(max_length=128, verbose_name='address')
    city = models.CharField(max_length=64)
    state = USStateField()
    zip_code = USZipCodeField(max_length=5)
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=128, null=True, blank=True)
    website = models.URLField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'{self.name} -- {self.city}, {self.state}'

class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    bowling_centers = models.ManyToManyField(BowlingCenter, related_name='%(class)s_bowling_center')

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract = True

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
    
class LeagueRoster(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league_rosters')
    date = models.DateField()

    def __str__(self):
        return f'{self.league.name} -- {self.date.strftime('%m/%d/%y')}'
    
class LeagueBowlerSidepotEntry(models.Model):
    bowler_entry = models.ForeignKey('LeagueBowlerEntry', on_delete=models.CASCADE, related_name='league_sidepot_entries')
    sidepot = GenericRelation(LeagueSidepot)
    entry_count = models.PositiveIntegerField(default=1)

    def clean(self):
        if not self.sidepot.allow_multiple_entries and self.entry_count > 1:
            raise ValidationError(f'Multiple entries are not allowed for {self.sidepot.name}')
        
    def __str__(self):
        return f'{self.bowler_entry.bowler} -- {self.sidepot.name} x {self.entry_count}'
    
class LeagueBowlerEntry(models.Model):
    league_roster = models.ForeignKey(LeagueRoster, on_delete=models.CASCADE, related_name='league_bowler_entries')
    bowler = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sidepots = models.ManyToManyField(LeagueSidepot, through=LeagueBowlerSidepotEntry, related_name='league_bowler_entries')

    def __str__(self):
        return f'{self.league_roster.league.name} -- {self.league_roster.date.strftime('%m/%d/%y')} -- {self.bowler}'

class Tournament(Event):
    directors = models.ManyToManyField(Profile, related_name='tournament_director')