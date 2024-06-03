from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import uuid

# Create your models here.
class Sidepot(models.Model):
    name = models.CharField(max_length=64)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    entry_fee = models.DecimalField(max_digits=6, decimal_places=2)
    payout_ratio = models.PositiveSmallIntegerField(default=6, validators=[MinValueValidator(2)])
    allow_multiple_entries = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

class HandicapSidepot(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    hdcp_percent = models.PositiveIntegerField(max_digits=3, validators=[MaxValueValidator(100)])
    base_average = models.PositiveIntegerField(max_digits=3, validators=[MaxValueValidator(300)])

    class Meta:
        abstract = True

class HighGame(Sidepot):
    name = models.CharField(max_length=64, default='High Game Pot', editable=False)

class HandicapHighGame(Sidepot, HandicapSidepot):
    name = models.CharField(max_length=64, default='Handicap High Game Pot', editable=False)
    
class HighSeries(Sidepot):
    name = models.CharField(max_length=64, default='High Series Pot', editable=False)

class HandicapHighSeries(Sidepot, HandicapSidepot):
    name = models.CharField(max_length=64, default='Handicap High Series Pot', editable=False)
    
class WinnerTakeAll(Sidepot):
    name = models.CharField(max_length=64, default='Winner Take All Pot', editable=False)

class HandicapWinnerTakeAll(Sidepot, HandicapSidepot):
    name = models.CharField(max_length=64, default='Handicap Winner Take All Pot', editable=False)
    
class Eliminator(Sidepot):
    name = models.CharField(max_length=64, default='Eliminator', editable=False)
    reverse = models.BooleanField(default=False)

    def __str__(self):
        name = str(self.name)

        if self.reverse:
            name = f'Reverse {name}' 

        return name

class HandicapEliminator(Sidepot, HandicapSidepot):
    name = models.CharField(max_length=64, default='Handicap Eliminator', editable=False)
    reverse = models.BooleanField(default=False)

    def __str__(self):
        name = str(self.name)

        if self.reverse:
            name = f'Reverse {name}' 

        return name

class MysteryDoubles(Sidepot):
    name = models.CharField(max_length=64, default='Mystery Doubles', editable=False)
    allow_multiple_entries = models.BooleanField(default=True, editable=False)

class HandicapMysteryDoubles(Sidepot, HandicapSidepot):
    name = models.CharField(max_length=64, default='Handicap Mystery Doubles', editable=False)
    allow_multiple_entries = models.BooleanField(default=True, editable=False)

# BRACKETS

# class Brackets(Sidepot):
#     name = models.CharField(max_length=64, default='Brackets', editable=False)
#     allow_multiple_entries = models.BooleanField(default=True, editable=False)
#     reverse = models.BooleanField(default=False)

#     def __str__(self):
#         name = str(self.name)

#         if self.reverse:
#             name = f'Reverse {name}' 

#         return name

# class HandicapBrackets(Sidepot, HandicapSidepot):
#     name = models.CharField(max_length=64, default='Handicap Brackets', editable=False)
#     allow_multiple_entries = models.BooleanField(default=True, editable=False)
#     reverse = models.BooleanField(default=False)

#     def __str__(self):
#         name = str(self.name)

#         if self.reverse:
#             name = f'Reverse {name}' 

#         return name