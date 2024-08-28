from django.forms import inlineformset_factory
from .models import Roster,RosterEntry, Game
from .forms import GameInputForm, RosterEntryScoreForm

GameInputFormSet = inlineformset_factory(
    RosterEntry,
    Game,
    form=GameInputForm,
    extra=0,
    can_delete=False,
)

ScoreVerificationFormSet = inlineformset_factory(
    Roster,
    RosterEntry,
    form=RosterEntryScoreForm,
    extra=0,
    can_delete=False,
)