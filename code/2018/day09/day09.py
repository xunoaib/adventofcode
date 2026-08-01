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
        self.current = Node(value)

    def pop(self):
        n = self.current
        n.ccw.cw = n.cw
        n.cw.ccw = n.ccw
        self.current = n.cw
        return n.value

    def insert(self, value: int):
        m1 = self.current.cw
        m2 = self.current.cw.cw
        self.current = m1.cw = m2.ccw = Node(value, cw=m2, ccw=m1)

    def move_ccw(self, steps: int):
        for _ in range(steps):
            self.current = self.current.ccw


def solve(last_marble: int):
    scores = Counter()

    marble = 1
    player = 1
    circle = LinkedList(0)

    while marble < last_marble:
        if marble % 23 == 0:
            scores[player] += marble
            circle.move_ccw(7)
            scores[player] += circle.pop()
        else:
            circle.insert(marble)

        marble += 1
        player = (player + 1) % NUM_PLAYERS

    return max(scores.values())


a1 = solve(LAST_MARBLE)
print('part1:', a1)

a2 = solve(LAST_MARBLE * 100)
print('part2:', a2)

assert a1 == 373597
assert a2 == 2954067253
