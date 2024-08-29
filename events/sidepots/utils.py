from events.models import RosterEntry

class BracketNode:
    def __init__(self, left=None, right=None):
        self.matchup = None
        self.left_child = left
        self.right_child = right

    def __eq__(self, other_node):
        return self.matchup == other_node.matchup

    def set_node(self, top, bottom):
        top = [top] if type(top) == RosterEntry else top
        bottom = [bottom] if type(top) == RosterEntry else bottom
        self.matchup = set(top) | set(bottom)

    def is_set(self):
        return bool(self.matchup)

                    

class Bracket:
    def __init__(self):
        nodes = [BracketNode() for i in range(4)]
        self.round_one = [node for node in nodes]

        for i in range(2):
            left = nodes.pop(0)
            right = nodes.pop(0)
            nodes.append(BracketNode(left, right))

        self.round_two = nodes
        self.final = BracketNode(nodes[0], nodes[1])
        self.bowler_list = set()
        self.round_list_map = {
            1: self.round_one,
            2: self.round_two,
            3: self.final,
        }

    def set_node(self, new_node, round_num):
        for node in self.round_list_map[round_num]:
            if not node.is_set():
                node.matchup = new_node.matchup
                bowler_list |= node.matchup
                return

        raise Exception # preferably custom

                    

    def is_full(self):
        return all((node.is_set() for node in self.round_one))