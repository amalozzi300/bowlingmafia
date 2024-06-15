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
            'allow_multiple_entries',
            'entry_fee',
            'payout_ratio',
            'games_used',
            'is_reverse',
        ]

    def __init__(self, *args, **kwargs):
        super(LeagueSidepotForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'league-sidepot__input'})

class CreateLeagueRosterForm(ModelForm):
    class Meta:
        model = Roster
        fields = ['date']

    def __init__(self, *args, **kwargs):
        super(CreateLeagueRosterForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'league_roster__input'})