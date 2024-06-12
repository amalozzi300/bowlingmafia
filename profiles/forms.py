from django.forms import ModelForm
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
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile_image',
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'edit-account__input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'name', 
            'email', 
            'subject', 
            'body',
        ]