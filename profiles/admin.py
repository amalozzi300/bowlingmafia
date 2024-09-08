from django.contrib import admin

from profiles.models import Message, Profile

admin.site.register(Profile)
admin.site.register(Message)
