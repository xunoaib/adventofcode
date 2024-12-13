#!/usr/bin/env python3
import re
import sys
from itertools import batched

from z3 import Int, Ints, Optimize, Solver, sat

lines = [line for line in sys.stdin.read().splitlines() if line.strip()]

a1 = a2 = 0

for a,b,c in batched(lines, 3):
    a_x = a_y = b_x = b_y = p_x = p_y = 0
    if m := re.match(r'.*: X+(.*), Y+(.*)', a):
        a_x, a_y = map(int, m.groups())
    if m := re.match(r'.*: X+(.*), Y+(.*)', b):
        b_x, b_y = map(int, m.groups())
    if m := re.match(r'.*: X=(.*), Y=(.*)', c):
        p_x, p_y = map(int, m.groups())

    zax, zay, zbx, zby, zpx, zpy = Ints('zax zay zbx zby zpx zpy')
    zac, zac, zbc, zbc, = Ints('zaxc zayc zbxc zbyc')
    tokens = Int('tokens')

    s = Optimize()
    s.add(p_x == zac * a_x + zbc * b_x)
    s.add(p_y == zac * a_y + zbc * b_y)
    s.add(zac >= 0)
    s.add(zbc >= 0)
    s.add(tokens == (3 * zac + 1 * zbc))
    s.minimize(tokens)

    if s.check() == sat:
        m = s.model()
        vals = [m[x].as_long() for x in [zac, zbc]]
        print(vals)
        print(m[tokens].as_long())
        a1 += m[tokens].as_long()


print('part1:', a1)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
