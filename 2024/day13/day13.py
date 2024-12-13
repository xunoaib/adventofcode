#!/usr/bin/env python3
import re
import sys
from itertools import batched

from z3 import Ints, Optimize, sat

lines = [line for line in sys.stdin.read().splitlines() if line.strip()]

def solve(prize_offset):
    tot = 0
    for a,b,c in batched(lines, 3):
        a_x = a_y = b_x = b_y = p_x = p_y = 0
        if m := re.match(r'.*: X+(.*), Y+(.*)', a):
            a_x, a_y = map(int, m.groups())
        if m := re.match(r'.*: X+(.*), Y+(.*)', b):
            b_x, b_y = map(int, m.groups())
        if m := re.match(r'.*: X=(.*), Y=(.*)', c):
            p_x, p_y = map(int, m.groups())
            p_x += prize_offset
            p_y += prize_offset

        zac, zac, zbc, zbc, tokens = Ints('zaxc zayc zbxc zbyc tokens')

        s = Optimize()
        s.add(p_x == zac * a_x + zbc * b_x)
        s.add(p_y == zac * a_y + zbc * b_y)
        s.add(zac >= 0)
        s.add(zbc >= 0)
        s.add(tokens == 3 * zac + 1 * zbc)
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
