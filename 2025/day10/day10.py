import re
import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

from z3 import Int, Optimize, Solver, sat

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
            cost, jolts = q.pop(0)

            if jolts == self.goal_jolts:
                return cost

            for n in self.neighbors(jolts):
                if n not in seen:
                    seen.add(n)
                    q.append((cost + 1, n))

        assert False

    def solvez(self):
        n = len(self.buttons)
        nj = len(self.goal_jolts)
        presses = [Int(f'presses{i}') for i in range(n)]
        outputs = [Int(f'o{i}') for i in range(nj)]

        s = Optimize()
        for p in presses:
            s.add(p >= 0)

        output_accs = {i: 0 for i in range(nj)}

        for bidx, bs in enumerate(self.buttons):
            for b in bs:
                output_accs[b] += presses[bidx]

        for i, o in enumerate(outputs):
            s.add(o == self.goal_jolts[i])
            s.add(o == output_accs[i])

        s.minimize(sum(presses))

        assert s.check() == sat

        m = s.model()
        return sum(m[p].as_long() for p in presses)

        # button1 = (2,3,4,5,6,7,8)
        # button2 = (0,1,2,3,7)
        # button3 = (1,2,3,4,8)
        # button4 = (1,2,3,4,5,6,8)
        # button5 = (0,4,6,7,8)
        # button6 = (4,6,7)
        # button7 = (5)
        # button8 = (0,1,3,7,8)
        # totals  = {13,30,32,41,36,25,29,24,45}

        # for p, o in zip(presses, outputs):
        #     s.add(o == p)

    def neighbors(self, jolts):
        for bs in self.buttons:
            njolts = list(jolts)
            for b in bs:
                njolts[b] += 1
                if njolts[b] > self.goal_jolts[b]:
                    break
            else:
                yield tuple(njolts)


aa = bb = 0
for line in lines:
    # aa += Machine(line).solve()
    # x = Machine2(line).solve()
    x = Machine2(line).solvez()
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
