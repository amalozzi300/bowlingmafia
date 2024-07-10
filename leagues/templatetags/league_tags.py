from django import template

register = template.Library()

@register.filter
def get_league_sidepot_entry_count(roster_entry, sidepot):
    sidepot_entry = roster_entry.league_bowler_sidepot_entries.get(sidepot=sidepot)
    return sidepot_entry.entry_count