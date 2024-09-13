from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from bowlingmafia.leagues.forms import LeagueForm
from bowlingmafia.leagues.models import League


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
            league.bowling_centers.set(request.POST.getlist('bowling_centers'))
            league.save()

            return redirect('event_home', league.slug)

    context = {'form': form}
    return render(request, 'leagues/league_form.html', context=context)


# def league_profile(request, pk):
#     league = League.objects.get(id=pk)
#     context = {'league': league}
#     return render(request, 'leagues/league.html', context=context)


@login_required(login_url='login')
def edit_league(request, league_slug):
    league = get_object_or_404(League, slug=league_slug)
    form = LeagueForm(instance=league)

    if request.user.profile not in league.admins.all():
        raise PermissionDenied

    if request.method == 'POST':
        form = LeagueForm(request.POST, instance=league)

        if form.is_valid():
            form.save()

            return redirect('event_home', league.slug)

    context = {
        'league': league,
        'form': form,
    }
    return render(request, 'leagues/league_form.html', context=context)


# @login_required(login_url='login')
# def invite_admin(request, pk):
#     return render(request, 'coming_soon.html')

# @login_required(login_url='login')
# def register_sidepot(request, pk):
#     league = League.objects.get(id=pk)
#     form = LeagueSidepotForm(league)

#     if request.user.profile not in league.admins.all():
#         # raise 403 permission denied
#         pass

#     if request.method == 'POST':
#         form = LeagueSidepotForm(league, request.POST)

#         if form.is_valid():
#             sidepot = form.save(commit=False)
#             sidepot.event = league
#             sidepot.save()

#             return redirect('league', league.id)

#     context = {
#         'league': league,
#         'form': form,
#     }
#     return render(request, 'leagues/sidepot_form.html', context=context)

# @login_required(login_url='login')
# def edit_sidepot(request, league_pk, sidepot_pk):
#     league = League.objects.get(id=league_pk)
#     sidepot = league.sidepots.get(id=sidepot_pk)
#     form = LeagueSidepotForm(league, instance=sidepot)

#     if request.user.profile not in league.admins.all():
#         # raise 403 permission denied
#         pass

#     if request.method == 'POST':
#         form = LeagueSidepotForm(league, request.POST, instance=sidepot)

#         if form.is_valid():
#             form.save()

#             return redirect('league', league.id)

#     context = {
#         'league': league,
#         'sidepot': sidepot,
#         'form': form,
#     }
#     return render(request, 'leagues/sidepot_form.html', context=context)

# @login_required(login_url='login')
# def create_roster(request, pk):
#     league = League.objects.get(id=pk)
#     form = CreateRosterForm()

#     if request.user.profile not in league.admins.all():
#         # raise 403 permission denied
#         pass

#     if request.method == 'POST':
#         form = CreateRosterForm(request.POST)

#         if form.is_valid():
#             roster = form.save(commit=False)
#             roster.event = league
#             roster.save()

#             return redirect('league', league.id)

#     context = {
#         'league': league,
#         'form': form,
#     }
#     return render(request, 'leagues/create_roster_form.html', context=context)

# def roster_view(request, league_pk, roster_pk):
#     league = League.objects.get(id=league_pk)
#     roster = league.rosters.get(id=roster_pk)
#     signed_up_users = roster.roster_entries.all().values_list('bowler')

#     context = {
#         'league': league,
#         'roster': roster,
#         'signed_up_users': signed_up_users,
#     }
#     return render(request, 'leagues/roster.html', context=context)

# @login_required(login_url='login')
# def create_roster_entry(request, league_pk, roster_pk):
#     league = League.objects.get(id=league_pk)
#     roster = league.rosters.get(id=roster_pk)
#     form = RosterEntryForm(league=league)

#     if request.user.profile in roster.roster_entries.all().values_list('bowler'):
#         redirect() # to edit entry page

#     if request.method == 'POST':
#         form = RosterEntryForm(league, request.POST)

#         if form.is_valid():
#             empty_form = True
#             all_entry_counts = {}

#             for field_name, value in form.cleaned_data.items():
#                 if field_name.startswith('sidepot_'):
#                     sidepot_pk = field_name.split('_')[1]
#                     sidepot = league.sidepots.get(id=sidepot_pk)
#                     num_entries = value if sidepot.allow_multiple_entries else 1

#                     if value > 0:
#                         empty_form = False
#                         all_entry_counts[sidepot] = num_entries

#             if not empty_form:
#                 roster_entry = RosterEntry.objects.create(roster=roster, bowler=request.user.profile)

#                 for sidepot, entry_count in all_entry_counts.items():
#                     BowlerSidepotEntry.objects.create(
#                         roster_entry=roster_entry,
#                         sidepot=sidepot,
#                         entry_count=entry_count,
#                     )

#             return redirect('league_roster', league_pk, roster_pk)

#     context = {
#         'league': league,
#         'roster': roster,
#         'form': form,
#     }
#     return render(request, 'leagues/roster_entry_form.html', context=context)
