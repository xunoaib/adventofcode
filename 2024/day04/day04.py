#!/usr/bin/env python3

import sys

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def count(r_start, c_start):
    total = 0
    for roff, coff in DIRS:
        r, c = r_start, c_start
        for ch in 'MAS':
            r += roff
            c += coff
            if g.get((r,c)) != ch:
                break
        else:
            total += 1
    return total

g = {
    (r,c): ch
    for r, row in enumerate(sys.stdin)
    for c, ch in enumerate(row.strip())
}

a1 = sum(count(*p) for p, ch in g.items() if ch == 'X')
a2 = 0

for (r,c), ch in g.items():
    if ch == 'A':
        diag1 = {
            g.get((r-1, c-1)),
            g.get((r+1, c+1))
        }
        diag2 = {
            g.get((r+1, c-1)),
            g.get((r-1, c+1))
        }
        a2 += diag1 == diag2 == set('MS')

print('part1:', a1)
print('part2:', a2)

assert a1 == 2560
assert a2 == 1910
