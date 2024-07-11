from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel
import uuid

from profiles.models import Profile

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


class Event(PolymorphicModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_events')
    bowling_centers = models.ManyToManyField(BowlingCenter, related_name='events')
    is_archived = models.BooleanField(default=False)

    # class Meta:
    #     abstract = True

    def __str__(self):
        return str(self.name)
    
    
class Sidepot(models.Model):
    SIDEPOTS = {
        'HG': 'High Game',
        'HS': 'High Series',
        'WTA': 'Winner Takes All',
        'Elim': 'Eliminator',
        'MD': 'Mystery Doubles',
    }

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='sidepots')
    type = models.CharField(max_length=64, choices=SIDEPOTS)
    entry_fee = models.DecimalField(max_digits=6, decimal_places=2)
    payout_ratio = models.PositiveSmallIntegerField(default=6, validators=[MinValueValidator(2)])
    is_handicap = models.BooleanField(default=False)
    games_used = ArrayField(models.PositiveIntegerField(), blank=True, default=list)
    is_reverse = models.BooleanField(default=False, blank=True)
    allow_multiple_entries = models.BooleanField(default=False)

    @property
    def name(self):
        hdcp = 'Handicap' if self.is_handicap else 'Scratch'
        games = ''
        
        games_used = self.games_used[::-1] if self.is_reverse else self.games_used

        for game in games_used:
            games += f' {str(game)},'
        
        if games:
            games = f'(games{games[:-1]})'

        return f'{hdcp} {self.get_type_display()} {games}'
    
    def __str__(self):
        return f'{self.event.name} - {self.name}'
    

class Roster(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rosters')
    date = models.DateField()
    is_registration_open = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.event.name} -- {self.date.strftime("%m/%d/%y")}'
    

class RosterEntry(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='roster_entries')
    bowler = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='roster_entries')
    sidepots = models.ManyToManyField(Sidepot, through='BowlerSidepotEntry')
    handicap = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return f'{self.roster.event.name} -- {self.roster.date.strftime("%m/%d/%y")} -- {self.bowler}'
    

class BowlerSidepotEntry(models.Model):
    roster_entry = models.ForeignKey(RosterEntry, on_delete=models.CASCADE, related_name='bowler_sidepot_entries')
    sidepot = models.ForeignKey(Sidepot, on_delete=models.CASCADE)
    entry_count = models.PositiveIntegerField(default=0)

    def clean(self):
        if not self.sidepot.allow_multiple_entries and self.entry_count > 1:
            raise ValidationError(f'Multiple entries are not allowed for {self.sidepot.type}')
        
    def __str__(self):
        return f'{self.roster_entry.bowler.username} -- {self.sidepot.type} x {self.entry_count}'
    

class Game(models.Model):
    bowler = models.ForeignKey(RosterEntry, on_delete=models.CASCADE, related_name='game_scores')
    game_number = models.PositiveIntegerField()
    scr_score = models.PositiveIntegerField(validators=[MaxValueValidator(300)])

    class Meta:
        unique_together = ('bowler', 'game_number')
    
    @property
    def hdcp_score(self):
        if not self.scr_score:
            return 0

        hdcp_score = self.scr_score + self.bowler.handicap

        return hdcp_score if hdcp_score <= 300 else 300
    
    def __str__(self):
        return str(self.hdcp_score)