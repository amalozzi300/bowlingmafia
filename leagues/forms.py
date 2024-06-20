from django import forms
from django.forms import ModelForm

from .models import League, LeagueSidepot, Roster

class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = [
            'name',
            'start_date',
            'num_games',
            'bowling_centers',
        ]

    def __init__(self, *args, **kwargs):
        super(LeagueForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'league__input'})

class LeagueAdminInviteForm(forms.Form):
    admin_email = forms.EmailField(label='email_address', max_length=128)

class LeagueSidepotForm(ModelForm):
    class Meta:
        model = LeagueSidepot
        fields = [
            'type',
            'is_handicap',
            'entry_fee',
            'payout_ratio',
            'games_used',
            'is_reverse',
        ]

    def __init__(self, league, *args, **kwargs):
        super(LeagueSidepotForm, self).__init__(*args, **kwargs)

        choices = []

        for i in range(league.num_games):
            choices.append((f'{i + 1}', f'Game {i + 1}'))

        self.fields['games_used'] = forms.MultipleChoiceField(choices=choices)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'league-sidepot__input'})

        self.fields['type'].widget.attrs.update({'id': 'sidepot__type'})

    def save(self, commit=True):
        instance = super(LeagueSidepotForm, self).save(commit=False)
        multiple_entries_allowed = ['MD']
        needs_games_used_and_reverse = ['Elim']

        if instance.type not in needs_games_used_and_reverse:
            instance.games_used = []
            instance.is_reverse = False

        instance.allow_multiple_entries = True if instance.type in multiple_entries_allowed else False
        
        if commit:
            instance.save()

        return instance

class CreateLeagueRosterForm(ModelForm):
    class Meta:
        model = Roster
        fields = ['date']

    def __init__(self, *args, **kwargs):
        super(CreateLeagueRosterForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'league_roster__input'})