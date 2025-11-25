import re
from collections import Counter

NUM_PLAYERS, LAST_MARBLE = map(int, re.findall(r'\d+', input()))


class Node:

    def __init__(
        self,
        value: int,
        cw: 'Node | None' = None,
        ccw: 'Node | None' = None,
    ):
        self.value = value
        self.cw: Node = cw or self
        self.ccw: Node = ccw or self


class LinkedList:

    def __init__(self, value: int):
        self.current_node = Node(value)

    def pop(self):
        n = self.current_node
        n.ccw.cw = n.cw
        n.cw.ccw = n.ccw
        self.current_node = n.cw
        return n.value

    def insert(self, value: int):
        m1 = self.current_node.cw
        m2 = self.current_node.cw.cw
        n = Node(value, cw=m2, ccw=m1)
        self.current_node = m1.cw = m2.ccw = n

    def move_ccw(self, steps: int):
        for _ in range(steps):
            self.current_node = self.current_node.ccw

    def move_cw(self, steps: int):
        for _ in range(steps):
            self.current_node = self.current_node.cw

    def print(self, player_turn: int):
        n = self.current_node
        while n.value != 0:
            n = n.ccw

        root = n
        nodes = [n]
        while n.cw != root:
            n = n.cw
            nodes.append(n)

        ns = ''.join(
            [
                f' \033[93m{"("+str(v.value)+")":>4}\033[0m'
                if v == self.current_node else f' {v.value:>4}'
                for i, v in enumerate(nodes)
            ]
        )

        print(f'[{player_turn}] {ns}')


def solve(last_marble: int):
    scores = Counter()

    marble_num = 1
    player_turn = 1
    circle = LinkedList(0)

    while marble_num < last_marble:
        if marble_num % 23 == 0:
            scores[player_turn] += marble_num
            circle.move_ccw(7)
            scores[player_turn] += circle.pop()
        else:
            circle.insert(marble_num)

        marble_num += 1
        player_turn = (player_turn + 1) % NUM_PLAYERS

    return max(scores.values())


a1 = solve(LAST_MARBLE)
print('part1:', a1)

a2 = solve(LAST_MARBLE * 100)
print('part2:', a2)

assert a1 == 373597
assert a2 == 2954067253
