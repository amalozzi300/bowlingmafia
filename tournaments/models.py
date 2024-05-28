from django.db import models
import uuid

from profiles.models import Profile

# Create your models here.
class Tournament(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=256, null=True, blank=True)
    directors = models.ManyToManyField(Profile, related_name='tournament_director')