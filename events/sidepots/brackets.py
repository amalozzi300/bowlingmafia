from collections import Counter
from random import randint

from events.sidepots.utils import Bracket, BracketNode
from events.models import BowlerSidepotEntry

def create_brackets(roster):
    """
    Upon the closing of sidepot registration, this creates the brackets for the passed in Roster
    """
    bracket_entrants = BowlerSidepotEntry.objects.filter(
        roster_entry__roster=roster,
        sidepot__type='BR',
    )
    master_list = []

    for entrant in bracket_entrants:
        for i in range(entrant.entry_count):
            master_list.append(entrant.roster_entry)

    num_entries = len(master_list)
    unique_entries = len(set(master_list))
    entries_per_entrant_map = Counter(master_list)

    # process data to ensure bracket requirements are met
        # len(master_list) % 8 == 0
        # entry count for each entrant must be <= int(len(master_list) / 8)
        # additional edge cases as we find them
    # will need to refund bowlers who have some bracket entries removed to meet bracket requirements

    # once all conditions are met to ensure there is at least one way of successfully compiling brackets
    all_nodes = []
    all_brackets = [Bracket()]
    max_brackets = int(len(master_list) / 8)
    count = 0

    while master_list:
        top = None
        bottom = None

        while top is None or top == bottom:
            index = randint(0, len(master_list) - 1)
            top = master_list.pop(index)
            index = randint(0, len(master_list) - 1)
            bottom = master_list.pop(index)
        
        new_node = BracketNode()
        new_node.set_node(top, bottom)

        if not new_node in all_nodes:
            for bracket in all_brackets:
                if not bracket.is_full():
                    bracket.set_node(new_node, 1)
                    all_nodes.append(new_node)
                    count = 0
                    break
                else:
                    new_bracket = Bracket()
                    new_bracket.set_node(new_node, 1)
                    all_brackets.append(new_bracket)
                    all_nodes.append(new_node)
                    count = 0

                    if len(all_brackets) > max_brackets:
                        # return falsey value, so outside loop can recall this function
                        pass
        else:
            if master_list:
                for bowler in new_node.matchup:
                    master_list.append(bowler)

                count += 1
            else:
                # return falsey value, so outside loop can recall this function
                pass

        if count == 10:
            # return falsey value, so outside loop can recall this function
            pass