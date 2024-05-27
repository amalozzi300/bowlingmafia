from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2',
        ]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'profile_image',
        ]

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'name', 
            'email', 
            'subject', 
            'body',
        ]