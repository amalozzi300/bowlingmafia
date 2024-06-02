from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import conf
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, MessageForm

# Create your views here.
def home(request):
    return redirect('login')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('account')
    
    if request.method == 'POST':
        username = request.POST['login_username'].lower()
        password = request.POST['login_password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR password is incorrect.')

    return render(request, 'profiles/login.html')

def logout_user(request):
    logout(request)
    messages.info(request, 'User was logged out.')
    return redirect('home')

def register_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'profiles/register.html', context=context)

def user_profile(request, pk):
    page = 'profile'
    profile = Profile.objects.get(id=pk)
    leagues = True if profile.league_admin.count() > 0 else False
    tournaments = True if profile.tournament_director.count() > 0 else False
    context = {
        'page': page,
        'profile': profile,
        'leagues': leagues,
        'tournaments': tournaments,
    }
    return render(request, 'profiles/profile.html', context=context)

@login_required(login_url='login')
def user_account(request):
    page = 'account'
    profile = request.user.profile
    leagues = True if profile.league_admin.count() > 0 else False
    tournaments = True if profile.tournament_director.count() > 0 else False
    context = {
        'page': page,
        'profile': profile,
        'leagues': leagues,
        'tournaments': tournaments,
    }
    return render(request, 'profiles/profile.html', context=context)

@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            if request.FILES.get('profile_image'):
                profile.profile_image = request.FILES['profile_image']
                profile.save()
            form.save()
            return redirect('account')
        
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'profiles/profile_form.html', context=context)
    
@login_required(login_url='login')
def inbox(request):
    page = 'inbox'
    profile = request.user.profile
    message_requests = profile.recipient.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {
        'page': page,
        'message_requests': message_requests,
        'unread_count': unread_count,
    }
    # return render(request, 'profiles/in_outbox.html', context=context)
    return render(request, 'coming_soon.html')

@login_required(login_url='login')
def outbox(request):
    page = 'outbox'
    profile = request.user.profile
    message_requests = profile.sender.all()
    context = {
        'page': page,
        'sent_messages': message_requests,
    }
    return render(request, 'profiles/in_outbox.html', context=context)

@login_required(login_url='login')
def view_message(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    
    if not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'coming_soon.html')

    # context = {'message': message}
    # return render(request, 'profiles/message.html', context=context)


@login_required(login_url='login')
def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    sender = request.user.profile

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.name = f'{sender.first_name} {sender.last_name}'
            message.email = sender.email
            message.save()

            messages.success(request, 'Your message was sent successfully!')
            return redirect('outbox')
        
    context = {
        'recipient': recipient,
        'form': form,
    }
    # return render(request, 'profiles/message_form.html', context=context)
    return render(request, 'coming_soon.html')
