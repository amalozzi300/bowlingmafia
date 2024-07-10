from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
import uuid

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
    bowling_centers = models.ManyToManyField(BowlingCenter, related_name='%(class)s_bowling_centers')
    is_archived = models.BooleanField(default=False)

    class Meta:
        abstract = True

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
    type = models.CharField(max_length=64, choices=SIDEPOTS)
    entry_fee = models.DecimalField(max_digits=6, decimal_places=2)
    payout_ratio = models.PositiveSmallIntegerField(default=6, validators=[MinValueValidator(2)])
    is_handicap = models.BooleanField(default=False)
    games_used = ArrayField(models.PositiveIntegerField(), blank=True, default=list)
    is_reverse = models.BooleanField(default=False, blank=True)
    allow_multiple_entries = models.BooleanField(default=False)

    class Meta:
        abstract = True

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
    

class Game(models.Model):
    game_number = models.PositiveIntegerField()
    scr_score = models.PositiveIntegerField(validators=[MaxValueValidator(300)])
    hdcp_score = models.PositiveIntegerField(validators=[MaxValueValidator(300)])

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.hdcp_score)