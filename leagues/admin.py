from django.contrib import admin

from .models import (
    BowlerSidepotEntry,
    Game,
    League,
    LeagueSidepot,
    Roster,
    RosterEntry,
)

# Register your models here.
admin.site.register(BowlerSidepotEntry)
admin.site.register(Game)
admin.site.register(League)
admin.site.register(LeagueSidepot)
admin.site.register(Roster)
admin.site.register(RosterEntry)