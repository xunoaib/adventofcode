#!/usr/bin/env python3
import re
import sys
from itertools import batched

from z3 import Ints, Optimize, sat

lines = [line for line in sys.stdin.read().splitlines() if line.strip()]

def solve(prize_offset):
    tot = 0
    for a,b,c in batched(lines, 3):
        a_x, a_y = map(int, re.match(r'.*: X+(.*), Y+(.*)', a).groups())
        b_x, b_y = map(int, re.match(r'.*: X+(.*), Y+(.*)', b).groups())
        p_x, p_y = map(int, re.match(r'.*: X=(.*), Y=(.*)', c).groups())
        p_x += prize_offset
        p_y += prize_offset

        a, b, tokens = Ints('a b tokens')

        s = Optimize()
        s.add(p_x == a * a_x + b * b_x)
        s.add(p_y == a * a_y + b * b_y)
        s.add(a >= 0)
        s.add(b >= 0)
        s.add(tokens == 3 * a + 1 * b)
        s.minimize(tokens)

        if s.check() == sat:
            tot += s.model()[tokens].as_long()

    return tot

a1 = solve(0)
a2 = solve(10000000000000)

print('part1:', a1)
print('part2:', a2)

assert a1 == 26810
assert a2 == 108713182988244
