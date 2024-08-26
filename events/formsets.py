from django.forms import formset_factory, inlineformset_factory
from .models import RosterEntry, Game
from .forms import GameInputForm

GameInputFormSet = inlineformset_factory(
    RosterEntry,
    Game,
    form=GameInputForm,
    extra=0,
    can_delete=False,
)
