from django.contrib import admin
from .models import Message, Profile

# Register your models here.
admin.site.register(Message)
admin.site.register(Profile)