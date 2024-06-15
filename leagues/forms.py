from django import forms
from django.forms import ModelForm

from .models import League, LeagueSidepot

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
            field.widget.attrs.update({'class': 'edit-league__input'})

class LeagueAdminInviteForm(forms.Form):
    admin_email = forms.EmailField(label='email_address', max_length=128)

class RegisterSidepotForm(ModelForm):
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
        super(RegisterSidepotForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'register-sidepot__input'})