from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import(
    Event,
    Sidepot, 
    Roster,
    RosterEntry,
    BowlerSidepotEntry,
    Game,
)
from .forms import(
    RegisterSidepotForm,
    CreateRosterForm,
    RosterEntryForm,
)
from leagues.models import League
from tournaments.models import Tournament

def event_homepage(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    form = CreateRosterForm()

    if request.user.profile not in event.admins.all():
        # raise 403 permission denied
        pass

    if request.method == 'POST':
        form = CreateRosterForm(request.POST)

        if form.is_valid():
            roster = form.save(commit=False)
            roster.event = event 
            roster.save()

            return redirect('event_home', event.slug)

    event_type = 'League' if type(event) is League else 'Tournament'
    context = {
        'event': event,
        'type': event_type,
        'form': form,
    }
    return render(request, 'events/event_homepage.html', context=context)

@login_required(login_url='login')
def invite_admin(request, event_slug):
    return render(request, 'coming_soon.html')

@login_required(login_url='login')
def register_sidepot(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    form = RegisterSidepotForm(event)

    if request.user.profile not in event.admins.all():
        # raise 403 permission denied
        pass

    if request.method == 'POST':
        form = RegisterSidepotForm(event, request.POST)

        if form.is_valid():
            sidepot = form.save(commit=False)
            sidepot.event = event
            sidepot.save()
            
            return redirect('event_home', event.slug)

    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'events/register_sidepot_form.html', context=context)

@login_required(login_url='login')
def edit_sidepot(request, event_slug, sidepot_slug):
    event = get_object_or_404(Event, slug=event_slug)
    sidepot = get_object_or_404(Sidepot, event=event, slug=sidepot_slug)
    form = RegisterSidepotForm(event, instance=sidepot)

    if request.user.profile not in event.admins.all():
        # raise 403 permission denied
        pass

    if request.method == 'POST':
        form = RegisterSidepotForm(event, request.POST, instance=sidepot)

        if form.is_valid():
            form.save()

            return redirect('event_home', event.slug)

    context = {
        'event': event,
        'sidepot': sidepot,
        'form': form,
    }
    return render(request, 'events/register_sidepot_form.html', context=context)

def roster_homepage(request, event_slug, roster_slug):
    event = get_object_or_404(Event, slug=event_slug)
    roster = get_object_or_404(Roster, event=event, slug=roster_slug)
    signed_up_users = roster.roster_entries.all().values_list('bowler', flat=True)

    context = {
        'event': event,
        'roster': roster,
        'signed_up_users': signed_up_users,
    }
    return render(request, 'events/roster_homepage.html', context=context)

@login_required(login_url='login')
def handle_close_registration(request, event_slug, roster_slug):
    event = get_object_or_404(Event, slug=event_slug)
    roster = get_object_or_404(Roster, event=event, slug=roster_slug)

    if request.user.profile not in event.admins.all():
        # raise 403 permission denied
        pass

    if roster.is_registration_open:
        roster.is_registration_open = False
        roster.save()

        for roster_entry in roster.roster_entries.all():
            games = []

            for i in range(event.num_games):
                games.append(Game(bowler=roster_entry, game_number=(i + 1)))

        Game.objects.bulk_create(games)  
        
    return redirect('roster_home', event_slug, roster_slug)
    
@login_required(login_url='login')
def create_roster_entry(request, event_slug, roster_slug):
    event = get_object_or_404(Event, slug=event_slug)
    roster = get_object_or_404(Roster, event=event, slug=roster_slug)
    form = RosterEntryForm(event)

    if request.user.profile in roster.roster_entries.all().values_list('bowler'):
        redirect() # to edit entry page
    
    if request.method == 'POST':
        form = RosterEntryForm(event, request.POST)

        if form.is_valid():
            empty_form = True
            all_entry_counts = {}

            for field_name, value in form.cleaned_data.items():
                if field_name.startswith('sidepot_'):
                    sidepot_pk = field_name.split('_')[1]
                    sidepot = event.sidepots.get(id=sidepot_pk)
                    num_entries = value if sidepot.allow_multiple_entries else 1

                    if value > 0:
                        empty_form = False
                        all_entry_counts[sidepot] = num_entries

            if not empty_form:
                roster_entry = RosterEntry.objects.create(roster=roster, bowler=request.user.profile)

                for sidepot, entry_count in all_entry_counts.items():
                    BowlerSidepotEntry.objects.create(
                        roster_entry=roster_entry,
                        sidepot=sidepot,
                        entry_count=entry_count,
                    )
            
            return redirect('roster_home', event_slug, roster_slug)

    context = {
        'event': event,
        'roster': roster,
        'form': form,
    }
    return render(request, 'events/roster_entry_form.html', context=context)