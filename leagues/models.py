from django.db import models
from django.utils.text import slugify

from events.models import Event
from profiles.models import Profile

class League(Event):
    # admins = models.ManyToManyField(Profile, related_name='is_league_admin')
    start_date = models.DateTimeField()
    num_games = models.PositiveIntegerField(default=3)

    def save(self, *args, **kwargs):
        year = self.start_date.strftime('%Y')
        self.slug = slugify(f'{self.name}_{year}_{self.id}')

        super(League, self).save(*args, **kwargs)