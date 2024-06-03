from django.contrib import admin

from .models import BowlingCenter, League, Tournament

# Register your models here.
admin.site.register(BowlingCenter)
admin.site.register(League)
admin.site.register(Tournament)