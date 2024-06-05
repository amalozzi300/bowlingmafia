from django.contrib import admin

from .models import (
    League,
    LeagueSidepot,
    Roster,
    BowlerSidepotEntry,
    RosterEntry,
)

# Register your models here.
admin.site.register(League)
admin.site.register(LeagueSidepot)
admin.site.register(Roster)
admin.site.register(BowlerSidepotEntry)
admin.site.register(RosterEntry)