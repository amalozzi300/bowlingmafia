from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import (
    EventRoster,
    EventSidepot,
    Game,
    RosterEntry,
)


class RegisterEventSidepotForm(forms.ModelForm):
    class Meta:
        model = EventSidepot
        fields = [
            'type',
            'is_handicap',
            'entry_fee',
            'payout_ratio',
            'games_used',
            'is_reverse',
        ]

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = []

        for i in range(event.num_games):
            choices.append((i + 1, f'Game {i + 1}'))

        self.fields['games_used'] = forms.MultipleChoiceField(
            choices=choices,
            widget=CheckboxSelectMultiple,
            required=False,
        )

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'sidepot__input'})

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
        instance = super().save(commit=False)
        multiple_entries_allowed = ['MD']
        needs_games_used_and_reverse = ['Elim']

        if instance.type not in needs_games_used_and_reverse:
            instance.games_used = []
            instance.is_reverse = False

        instance.allow_multiple_entries = True if instance.type in multiple_entries_allowed else False

        if commit:
            instance.save()

        return instance


class CreateEventRosterForm(forms.ModelForm):
    class Meta:
        model = EventRoster
        fields = ['date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'roster__input'})


class RosterEntryForm(forms.ModelForm):
    class Meta:
        model = RosterEntry
        fields = []

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sidepots = event.sidepots.all()

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

    def clean(self):
        cleaned_data = super().clean()

        for field, value in cleaned_data.items():
            if not value:
                cleaned_data[field] = 0


class GameInputForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['scr_score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['scr_score'].label = f'Game {self.instance.game_number}'


class RosterEntryScoreForm(forms.ModelForm):
    class Meta:
        model = RosterEntry
        fields = ['handicap']
