from django.db import models
from django.core.validators import MaxValueValidator

from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
import uuid

from profiles.models import Profile

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


class Bowler(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='bowler')
    handicap = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(300)])

    def __str__(self):
        return f'{self.profile.first_name} {self.profile.last_name}'


class Game(models.Model):
    game_number = models.PositiveIntegerField()
    scr_score = models.PositiveIntegerField(validators=[MaxValueValidator(300)])
    hdcp_score = models.PositiveIntegerField(validators=[MaxValueValidator(300)])

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.hdcp_score)