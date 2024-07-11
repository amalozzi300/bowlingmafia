from django.db import models

from events.models import Event
from profiles.models import Profile

class Tournament(Event):
    directors = models.ManyToManyField(Profile, related_name='is_tournament_director')
    num_qualifying_games = models.PositiveIntegerField(default=3)