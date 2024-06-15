from django.contrib import admin

from .models import (
    BowlerSidepotEntry,
    League,
    LeagueGame,
    LeagueSidepot,
    Roster,
    RosterEntry,
)

# Register your models here.
admin.site.register(BowlerSidepotEntry)
admin.site.register(League)
admin.site.register(LeagueGame)
admin.site.register(LeagueSidepot)
admin.site.register(Roster)
admin.site.register(RosterEntry)