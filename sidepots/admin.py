from django.contrib import admin

from .models import (
    HighGame,
    HandicapHighGame,
    HighSeries,
    HandicapHighSeries,
    WinnerTakeAll,
    HandicapWinnerTakeAll,
    Eliminator,
    HandicapEliminator,
    MysteryDoubles,
    HandicapMysteryDoubles,
)

# Register your models here.
admin.site.register(HighGame)
admin.site.register(HandicapHighGame)
admin.site.register(HighSeries)
admin.site.register(HandicapHighSeries)
admin.site.register(WinnerTakeAll)
admin.site.register(HandicapWinnerTakeAll)
admin.site.register(Eliminator)
admin.site.register(HandicapEliminator)
admin.site.register(MysteryDoubles)
admin.site.register(HandicapMysteryDoubles)

