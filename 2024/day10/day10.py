#!/usr/bin/env python3

import sys

DIRS = (-1, 0), (1, 0), (0, -1), (0, 1)


def neighbors4(r, c):
    for roff, coff in DIRS:
        if not (roff and coff):
            yield r + roff, c + coff


lines = sys.stdin.read().strip().split('\n')

g = {
    (r, c): int(ch)
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
    if ch != '.'
}

def find_trails(orig_r, orig_c):
    t1 = set()
    t2 = 0
    q = [(orig_r,orig_c)]
    while q:
        cur = q.pop()
        if g[cur] == 9:
            t1.add((orig_r,orig_c,*cur))
            t2 += 1
            continue
        for n in neighbors4(*cur):
            if g.get(n) == g[cur] + 1:
                q.append(n)
    return t1, t2

a1trails = set()
a2 = 0

for (r,c), v in g.items():
    if v == 0:
        t1, t2 = find_trails(r,c)
        a1trails |= t1
        a2 += t2

a1 = len(a1trails)

print('part1:', a1)
print('part2:', a2)

assert a1 == 496
assert a2 == 1120
