from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import League
from .forms import LeagueForm

# Create your views here.
@login_required(login_url='login')
def create_league(request):
    form = LeagueForm()

    if request.method == 'POST':
        pass

    context = {'form': form}
    return render(request, 'leagues/league_form.html', context=context)

def league_profile(request, pk):
    league = League.objects.get(id=pk)
    context = {'league': league}
    return render(request, 'leagues/league.html', context=context)

def edit_league(request, pk):
    pass