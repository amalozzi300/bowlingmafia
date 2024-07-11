from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import League
from events.models import(
    Sidepot,
    Roster,
    RosterEntry,
)

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

class LeagueSidepotForm(ModelForm):
    class Meta:
        model = Sidepot
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
            choices.append((i + 1, f'Game {i + 1}'))

        self.fields['games_used'] = forms.MultipleChoiceField(
            choices=choices,
            widget= CheckboxSelectMultiple,
            required=False,
        )

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'league-sidepot__input'})

        self.fields['type'].widget.attrs.update({'id': 'sidepot__type'})

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        games_used = cleaned_data.get('games_used')
        needs_games_used_and_reverse = ['Elim']

        if type in needs_games_used_and_reverse:
            if len(games_used) != 3:
                self.add_error('games_used', 'You must select exactly 3 games to be used.')

        if games_used:
            cleaned_data['games_used'] = [int(item) for item in games_used]

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

class CreateRosterForm(ModelForm):
    class Meta:
        model = Roster
        fields = ['date', 'is_registration_open']

    def __init__(self, *args, **kwargs):
        super(CreateRosterForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'league_roster__input'})

class RosterEntryForm(ModelForm):
    class Meta:
        model = RosterEntry
        fields = []

    def __init__(self, league, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sidepots = league.league_sidepots.all()

        for sidepot in sidepots:
            field_name = f'sidepot_{sidepot.id}'

            if sidepot.allow_multiple_entries:
                self.fields[field_name] = forms.IntegerField(
                    label=sidepot.name,
                    required=False,
                    min_value=0,
                    widget=forms.NumberInput(attrs={'data-entry-fee': sidepot.entry_fee}),
                )
            else:
                self.fields[field_name] = forms.BooleanField(
                    label=sidepot.name,
                    required=False,
                    widget=forms.CheckboxInput(attrs={'data-entry-fee': sidepot.entry_fee}),
                )