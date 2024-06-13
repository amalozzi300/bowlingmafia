from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import League
from .forms import LeagueForm

# Create your views here.
@login_required(login_url='login')
def create_league(request):
    form = LeagueForm()

    if request.method == 'POST':
        form = LeagueForm(request.POST)

        if form.is_valid():
            league = form.save()
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
        # raise 404 permission denied
        pass
    
    if request.method == 'POST':
        pass

    context = {
        'league': league,
        'form': form,
    }
    return render(request, 'leagues/league_form.html', context=context)


@login_required(login_url='login')
def invite_admin(request, pk):
    pass