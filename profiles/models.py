from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=64, unique=True, null=True)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=128, null=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_image = models.ImageField(
        upload_to='profiles/', 
        default='profiles/user_default.png', 
        null=True, 
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.username)


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        null=True, 
        blank=True,
    )
    recipient = models.ForeignKey(
        Profile, 
        on_delete=models.SET_NULL,
        related_name = 'received_messages',
        null=True, 
        blank=True,
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    subject = models.CharField(max_length=256, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_read', '-created']

    def __str__(self):
        return self.subject