from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from leagues.models import League

from .forms import CustomUserCreationForm, MessageForm, ProfileForm
from .models import Message, Profile


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
    return redirect('home')


def register_user(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('edit_account')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'profiles/register.html', context=context)


def user_profile(request, username):
    page = 'profile'
    profile = get_object_or_404(Profile, username=username)

    if request.user.profile.id == profile.id:
        return redirect('account')

    admined_events = profile.admined_events.all()
    admined_leagues = []
    admined_tournaments = []

    for event in admined_events:
        if type(event) is League:
            admined_leagues.append(event)
        else:
            admined_tournaments.append(event)

    leagues = True if len(admined_leagues) > 0 else False
    tournaments = True if len(admined_tournaments) > 0 else False
    context = {
        'page': page,
        'profile': profile,
        'leagues': leagues,
        'admined_leagues': admined_leagues,
        'tournaments': tournaments,
        'admined_tournaments': admined_tournaments,
    }
    return render(request, 'profiles/profile.html', context=context)


@login_required(login_url='login')
def user_account(request):
    page = 'account'
    profile = request.user.profile
    admined_events = profile.admined_events.all()
    admined_leagues = []
    admined_tournaments = []

    for event in admined_events:
        if type(event) is League:
            admined_leagues.append(event)
        else:
            admined_tournaments.append(event)

    leagues = True if len(admined_leagues) > 0 else False
    tournaments = True if len(admined_tournaments) > 0 else False
    context = {
        'page': page,
        'profile': profile,
        'leagues': leagues,
        'admined_leagues': admined_leagues,
        'tournaments': tournaments,
        'admined_tournaments': admined_tournaments,
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
def view_message(request, message_pk):
    recipient = request.user.profile
    message = get_object_or_404(Message, recipient=recipient, id=message_pk)

    if not message.is_read:
        message.is_read = True
        message.save()

    # context = {'message': message}
    # return render(request, 'profiles/message.html', context=context)
    return render(request, 'coming_soon.html')


@login_required(login_url='login')
def create_message(request, recipient_pk):
    sender = request.user.profile
    recipient = get_object_or_404(Profile, id=recipient_pk)
    form = MessageForm()

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
