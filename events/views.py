from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from leagues.models import League

from .forms import (
    CreateRosterForm,
    RegisterSidepotForm,
    RosterEntryForm,
    RosterEntryScoreForm,
)
from .formsets import GameInputFormSet, ScoreVerificationFormSet
from .models import (
    BowlerSidepotEntry,
    Event,
    Game,
    Roster,
    RosterEntry,
    Sidepot,
)


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
        redirect()  # to edit entry page

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


@login_required(login_url='login')
def user_game_score_input(request, event_slug, roster_slug):
    event = get_object_or_404(Event, slug=event_slug)
    roster = get_object_or_404(Roster, event=event, slug=roster_slug)

    if roster.is_registration_open:
        return redirect('roster_home', event_slug, roster_slug)

    roster_entry = get_object_or_404(RosterEntry, roster=roster, bowler=request.user.profile)
    form = RosterEntryScoreForm(instance=roster_entry)
    formset = GameInputFormSet(instance=roster_entry, queryset=roster_entry.game_scores.all())

    if request.method == 'POST':
        for key, val in request.POST.items():
            print(key, val)
        form = RosterEntryScoreForm(request.POST, instance=roster_entry)
        formset = GameInputFormSet(request.POST, instance=roster_entry, queryset=roster_entry.game_scores.all())

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('roster_home', event_slug, roster_slug)

    context = {
        'event': event,
        'roster': roster,
        'form': form,
        'formset': formset,
    }
    return render(request, 'events/score_input_form.html', context=context)


@login_required(login_url='login')
def score_verification(request, event_slug, roster_slug):
    event = get_object_or_404(Event, slug=event_slug)

    if request.user.profile not in event.admins.all():
        # raise 403 permission denied
        pass

    roster = get_object_or_404(Roster, event=event, slug=roster_slug)
    roster_entry_formset = ScoreVerificationFormSet(instance=roster, prefix='roster_entry')
    game_formsets = [
        GameInputFormSet(instance=form.instance, prefix=f'game-{index}')
        for index, form in enumerate(roster_entry_formset.forms)
    ]

    if request.method == 'POST':
        roster_entry_formset = ScoreVerificationFormSet(request.POST, instance=roster, prefix='roster_entry')
        game_formsets = []

        if roster_entry_formset.is_valid():
            roster_entries = roster_entry_formset.save(commit=False)

            for index, form in enumerate(roster_entry_formset.forms):
                entry = form.instance
                new_game_formset = GameInputFormSet(request.POST, instance=entry, prefix=f'game-{index}')
                game_formsets.append(new_game_formset)

            if all([gfs.is_valid() for gfs in game_formsets]):
                for entry in roster_entries:
                    entry.save()  # Save child instances

                for gfs in game_formsets:
                    gfs.save()  # Save grandchild instances

                return redirect('roster_home', event_slug, roster_slug)  # Replace with your success URL

    context = {
        'event': event,
        'roster': roster,
        'roster_entry_formset': roster_entry_formset,
        'game_formsets': game_formsets,
    }
    return render(request, 'events/score_verification_form.html', context)
