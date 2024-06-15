from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField

import uuid

# Create your models here.
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
    games_used = ArrayField(models.PositiveIntegerField())
    is_reverse = models.BooleanField(default=False)
    allow_multiple_entries = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_type_display()