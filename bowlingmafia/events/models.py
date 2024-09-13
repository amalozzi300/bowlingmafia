from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from localflavor.us.models import USStateField, USZipCodeField
from phonenumber_field.modelfields import PhoneNumberField
from polymorphic.models import PolymorphicModel
from profiles.models import Profile


class BowlingCenter(models.Model):
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
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_events')
    admins = models.ManyToManyField(Profile, related_name='admined_events')
    bowling_centers = models.ManyToManyField(BowlingCenter, related_name='events')
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.pk:
            # object does not exist in the database, so does not have pk value
            # pk value is needed for slug creation, so we temporarily save the object to create a pk value
            self.slug = slugify(f'temp_{self.name}_slug')
            super().save(*args, **kwargs)

        self.slug = slugify(f'{self.name}_{self.pk}')
        super().save(*args, **kwargs)


class EventBowler:
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    handicap = models.PositiveIntegerField(default=0, blank=True)


class EventSidepot(models.Model):
    SIDEPOTS = {
        'HG': 'High Game',
        'HS': 'High Series',
        'WTA': 'Winner Takes All',
        'Elim': 'Eliminator',
        'MD': 'Mystery Doubles',
        'BR': 'Brackets',
    }

    slug = models.SlugField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_sidepots')
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

    class Meta:
        unique_together = ('event', 'type', 'is_handicap', 'games_used', 'is_reverse')

    def __str__(self):
        return f'{self.event.name} - {self.name}'

    def save(self, *args, **kwargs):
        hdcp = 'hdcp' if self.is_handicap else 'scr'
        self.slug = slugify(f'{hdcp}-{self.get_type_display()}')
        super().save(*args, **kwargs)


class SidepotRoster:
    event_sidepot = models.ForeignKey(EventSidepot, on_delete=models.PROTECT, related_name='sidepot_rosters')
    # results
    # roster list (multiple roster entries, or multiple containers of roster entries -- ie brackets, mystery doubles pairs)


class EventRoster(models.Model):
    slug = models.SlugField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_rosters')
    date = models.DateField()
    is_registration_open = models.BooleanField(default=True)

    class Meta:
        unique_together = ('event', 'slug')

    def __str__(self):
        return f'{self.event.name} -- {self.date.strftime("%m/%d/%y")}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.date.strftime('%m-%d-%y'))
        super().save(*args, **kwargs)


# class RosterEntry(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
#     roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name='roster_entries')
#     bowler = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='roster_entries')
#     sidepots = models.ManyToManyField(Sidepot, through='BowlerSidepotEntry')
#    handicap = models.PositiveIntegerField(default=0, blank=True)


#     class Meta:
#         unique_together = ('roster', 'bowler')

#     def __str__(self):
#         return f'{self.roster.event.name} -- {self.roster.date.strftime("%m/%d/%y")} -- {self.bowler}'


# class BowlerSidepotEntry(models.Model):
#     roster_entry = models.ForeignKey(RosterEntry, on_delete=models.CASCADE, related_name='bowler_sidepot_entries')
#     sidepot = models.ForeignKey(Sidepot, on_delete=models.CASCADE)
#     entry_count = models.PositiveIntegerField(default=0)

#     def clean(self):
#         if not self.sidepot.allow_multiple_entries and self.entry_count > 1:
#             raise ValidationError(f'Multiple entries are not allowed for {self.sidepot.type}')

#     def __str__(self):
#         return f'{self.roster_entry.bowler.username} -- {self.sidepot.type} x {self.entry_count}'


class RosterEntry:
    roster = models.ForeignKey(EventRoster, on_delete=models.PROTECT, related_name='roster_entries')
    bowler = models.ForeignKey(EventBowler, on_delete=models.PROTECT, related_name='roster_entries')
    sidepot = models.ForeignKey(SidepotRoster, on_delete=models.PROTECT, related_name='roster_entries')
    entry_count = models.PositiveIntegerField(default=0)

    def clean(self):
        if not self.sidepot.event_sidepot.allow_multiple_entries and self.entry_count > 1:
            raise ValidationError(f'Multiple entries are not allowed for {self.sidepot.type}')


class Game(models.Model):
    bowler = models.ForeignKey(EventBowler, on_delete=models.CASCADE, related_name='games')
    game_number = models.PositiveIntegerField()
    scr_score = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(300)])

    @property
    def hdcp_score(self):
        if not self.scr_score:
            return 0

        hdcp_score = self.scr_score + self.bowler.handicap

        return hdcp_score if hdcp_score <= 300 else 300

    class Meta:
        unique_together = ('bowler', 'game_number')

    def __str__(self):
        return str(self.hdcp_score)
