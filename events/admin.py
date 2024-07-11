from django.contrib import admin

from .models import(
    BowlingCenter,
    Sidepot,
    Roster,
    RosterEntry,
    BowlerSidepotEntry,
    Game,
)

admin.site.register(BowlingCenter)
admin.site.register(Sidepot)
admin.site.register(Roster)
admin.site.register(RosterEntry)
admin.site.register(BowlerSidepotEntry)
admin.site.register(Game)