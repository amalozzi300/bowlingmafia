from django.contrib import admin

from .models import (
    BowlingCenter, 
    League, 
    LeagueSidepot,
    LeagueRoster,
    LeagueBowlerSidepotEntry,
    LeagueBowlerEntry,
    Tournament,
)

# Register your models here.
admin.site.register(BowlingCenter)
admin.site.register(League)
admin.site.register(LeagueSidepot)
admin.site.register(LeagueRoster)
admin.site.register(LeagueBowlerSidepotEntry)
admin.site.register(LeagueBowlerEntry)
admin.site.register(Tournament)