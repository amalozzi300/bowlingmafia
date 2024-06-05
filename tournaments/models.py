from django.db import models

from common.models import Event
from profiles.models import Profile

# Create your models here.
class Tournament(Event):
    directors = models.ManyToManyField(Profile, related_name='tournament_director')