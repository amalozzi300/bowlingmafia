from django.forms import inlineformset_factory

from .forms import GameInputForm, RosterEntryScoreForm
from .models import EventRoster, Game, RosterEntry

GameInputFormSet = inlineformset_factory(
    RosterEntry,
    Game,
    form=GameInputForm,
    extra=0,
    can_delete=False,
)

ScoreVerificationFormSet = inlineformset_factory(
    EventRoster,
    RosterEntry,
    form=RosterEntryScoreForm,
    extra=0,
    can_delete=False,
)
