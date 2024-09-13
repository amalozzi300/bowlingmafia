from django.contrib import admin

from events.models import (
    BowlingCenter,
    EventBowler,
    EventRoster,
    EventSidepot,
    Game,
    RosterEntry,
)

admin.site.register(BowlingCenter)
admin.site.register(EventSidepot)
admin.site.register(EventRoster)
admin.site.register(RosterEntry)
admin.site.register(EventBowler)
admin.site.register(Game)
