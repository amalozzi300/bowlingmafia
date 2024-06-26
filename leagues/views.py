from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import League
from .forms import LeagueForm, LeagueSidepotForm, CreateRosterForm, RosterEntryForm

# Create your views here.
@login_required(login_url='login')
def create_league(request):
    form = LeagueForm()

    if request.method == 'POST':
        form = LeagueForm(request.POST)

        if form.is_valid():
            league = form.save(commit=False)
            league.owner = request.user.profile
            league.save()
            league.admins.add(request.user.profile)
            league.save()

            return redirect('league', league.id)

    context = {'form': form}
    return render(request, 'leagues/league_form.html', context=context)

def league_profile(request, pk):
    league = League.objects.get(id=pk)
    context = {'league': league}
    return render(request, 'leagues/league.html', context=context)

@login_required(login_url='login')
def edit_league(request, pk):
    league = League.objects.get(id=pk)
    form = LeagueForm(instance=league)

    if request.user.profile not in league.admins.all():
        # raise 403 permission denied
        pass
    
    if request.method == 'POST':
        form = LeagueForm(request.POST, instance=league)

        if form.is_valid():
            form.save()

            return redirect('league', league.id)

    context = {
        'league': league,
        'form': form,
    }
    return render(request, 'leagues/league_form.html', context=context)

@login_required(login_url='login')
def invite_admin(request, pk):
    return render(request, 'coming_soon.html')

@login_required(login_url='login')
def register_sidepot(request, pk):
    league = League.objects.get(id=pk)
    form = LeagueSidepotForm(league)

    if request.user.profile not in league.admins.all():
        # raise 403 permission denied
        pass

    if request.method == 'POST':
        form = LeagueSidepotForm(league, request.POST)

        if form.is_valid():
            sidepot = form.save(commit=False)
            sidepot.league = league
            sidepot.save()
            
            return redirect('league', league.id)

    context = {
        'league': league,
        'form': form,
    }
    return render(request, 'leagues/sidepot_form.html', context=context)

@login_required(login_url='login')
def edit_sidepot(request, league_pk, sidepot_pk):
    league = League.objects.get(id=league_pk)
    sidepot = league.league_sidepots.get(id=sidepot_pk)
    form = LeagueSidepotForm(league, instance=sidepot)

    if request.user.profile not in league.admins.all():
        # raise 403 permission denied
        pass

    if request.method == 'POST':
        form = LeagueSidepotForm(league, request.POST, instance=sidepot)

        if form.is_valid():
            form.save()

            return redirect('league', league.id)

    context = {
        'league': league,
        'sidepot': sidepot,
        'form': form,
    }
    return render(request, 'leagues/sidepot_form.html', context=context)

@login_required(login_url='login')
def create_roster(request, pk):
    league = League.objects.get(id=pk)
    form = CreateRosterForm()

    if request.user.profile not in league.admins.all():
        # raise 403 permission denied
        pass

    if request.method == 'POST':
        form = CreateRosterForm(request.POST)

        if form.is_valid():
            roster = form.save(commit=False)
            roster.league = league
            roster.save()

            return redirect('league', league.id)

    context = {
        'league': league,
        'form': form,
    }
    return render(request, 'leagues/create_roster_form.html', context=context)

def roster_view(request, league_pk, roster_pk):
    league = League.objects.get(id=league_pk)
    roster = league.league_rosters.get(id=roster_pk)
    bowler_entry_fees = {}
    
    for entry in roster.league_roster_entries.all():
        cost = 0
        bowler = entry.bowler

        for sidepot in entry.sidepots.all():
            cost += sidepot.entry_fee

        bowler_entry_fees[bowler] = cost

    context = {
        'league': league,
        'roster': roster,
        'bowler_entry_fees': bowler_entry_fees
    }
    return render(request, 'leagues/roster.html', context=context)

def create_roster_entry(request, league_pk, roster_pk):
    league = League.objects.get(id=league_pk)
    roster = league.league_rosters.get(id=roster_pk)
    form = RosterEntryForm

    if request.method == 'POST':
        form = RosterEntryForm(request.POST)

        if form.is_valid():
            form.save()

    context = {
        'league': league,
        'roster': roster,
        'form': form,
    }
    return render(request, 'leagues/roster_entry_form.html', context=context)