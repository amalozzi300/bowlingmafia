from django import template

register = template.Library()


@register.filter
def dict_lookup(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_sidepot_entry_count(roster_entry, sidepot):
    sidepot_entry = roster_entry.bowler_sidepot_entries.get(sidepot=sidepot)
    return sidepot_entry.entry_count if sidepot_entry.entry_count else 0


@register.filter
def get_total_entry_fee(roster_entry):
    total_entry_fee = 0

    for sidepot in roster_entry.sidepots.all():
        entry_count = roster_entry.bowler_sidepot_entries.get(sidepot=sidepot).entry_count
        total_entry_fee += sidepot.entry_fee * entry_count

    return total_entry_fee
