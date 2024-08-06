from django.db import models
from django.utils.text import slugify

from events.models import Event

class League(Event):
    start_date = models.DateTimeField()
    num_games = models.PositiveIntegerField(default=3)

    def save(self, *args, **kwargs):
        year = self.start_date.strftime('%Y')
        self.slug = slugify(f'{self.name}_{year}_{self.id}')

        super(League, self).save(*args, **kwargs)