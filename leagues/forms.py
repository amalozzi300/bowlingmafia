from django.forms import ModelForm

from .models import League

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

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'edit-league__input'})