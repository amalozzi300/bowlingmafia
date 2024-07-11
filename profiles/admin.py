from django.contrib import admin
from .models import Message, Profile

admin.site.register(Profile)
admin.site.register(Message)
