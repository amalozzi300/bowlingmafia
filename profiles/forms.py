from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [

        ]