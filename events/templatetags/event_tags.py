from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_sidepot_entry_count(roster_entry, sidepot):
    sidepot_entry = roster_entry.bowler_sidepot_entries.get(sidepot=sidepot)
    return sidepot_entry.entry_count