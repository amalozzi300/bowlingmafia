from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile
from .forms import ProfileCreationForm

# Create your views here.
