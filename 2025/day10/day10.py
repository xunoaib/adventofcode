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

        assert False

    def neighbors(self, state):
        for bs in self.buttons:
            s = list(state)
            for b in bs:
                s[b] = not s[b]
            yield tuple(s)


class Machine2:

    def __init__(self, line):
        lights, *buttons, req = [g[1:-1] for g in line.split(' ')]
        self.goal_lights = tuple(ch == '#' for ch in lights)
        self.lights = (False, ) * len(self.goal_lights)
        self.goal_jolts = tuple(map(int, req.split(',')))
        self.jolts = (0, ) * len(self.goal_jolts)
        self.buttons = tuple(tuple(map(int, g.split(','))) for g in buttons)
        self.mode = True

    def solve(self):
        q = [(0, self.jolts)]
        seen = {q[0][1]}
        while q:
            cost, jolts = heappop(q)

            if jolts == self.goal_jolts:
                return cost

            for n in self.neighbors(jolts):
                if n not in seen:
                    seen.add(n)
                    heappush(q, (cost + 1, n))

        assert False

    def neighbors(self, jolts):
        for bs in self.buttons:
            njolts = list(jolts)
            for b in bs:
                njolts[b] += 1
            yield tuple(njolts)


aa = bb = 0
for line in lines:
    aa += Machine(line).solve()
    x = Machine2(line).solve()
    print(x)
    bb += x

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
