import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    return {(r + roff, c + coff) for roff, coff in DIRS}


aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

ROWS = max(r for r, c in grid) + 1

bugs = frozenset(p for p, ch in grid.items() if ch == '#')
valid = set(grid)

seen = set()

while bugs not in seen:
    print(bugs)
    seen.add(bugs)

    survivors = {p for p in bugs if len(neighbors4(*p) & bugs) == 1}
    infested = {
        p
        for p in valid
        if p not in bugs and len(neighbors4(*p) & bugs) in (1, 2)
    }

    bugs = frozenset(survivors | infested)
    print(bugs)

aa = sum(2**(r * ROWS + c) for r, c in bugs)

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
