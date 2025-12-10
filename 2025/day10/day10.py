import re
import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')


class Machine:

    def __init__(self, line):
        lights, *buttons, req = [g[1:-1] for g in line.split(' ')]
        self.goal = tuple(ch == '#' for ch in lights)
        self.buttons = tuple(tuple(map(int, g.split(','))) for g in buttons)
        self.req = tuple(map(int, req.split(',')))
        self.state = (False, ) * len(self.goal)

    def solve(self):
        q = [(0, self.state)]
        seen = {self.state}
        while q:
            cost, s = q.pop(0)
            if s == self.goal:
                return cost

            for n in self.neighbors(s):
                if n not in seen:
                    seen.add(n)
                    q.append((cost + 1, n))

    def neighbors(self, state):
        for bs in self.buttons:
            s = list(state)
            for b in bs:
                s[b] = not s[b]
            yield tuple(s)


aa = 0
for line in lines:
    m = Machine(line)
    x = m.solve()
    aa += x

# grid = {
#     (r, c): ch
#     for r, line in enumerate(lines)
#     for c, ch in enumerate(line)
# }

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
