from django.contrib import admin

from bowlingmafia.profiles.models import Message, Profile

admin.site.register(Profile)
admin.site.register(Message)
