import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None


def neighbors8(r, c):
    for roff, coff in product([-1, 0, 1], repeat=2):
        if roff or coff:
            yield r + roff, c + coff


s = sys.stdin.read()
lines = s.strip().split('\n')

grid = {
    (r, c): ch
    for r, line in enumerate(lines)
    for c, ch in enumerate(line)
}

g = grid.copy()


def accessible(g):

    r = []
    for p in g:
        count = sum(1 for n in neighbors8(*p) if n in g)
        if count < 4:
            r.append(p)
    return r


grid = {k for k, v in grid.items() if v == '@'}

aa = len(list(accessible(grid)))

oglen = l = len(grid)
while acc := set(accessible(grid)):
    grid -= acc

bb = oglen - len(grid)

# maxr = max(r for r, c in grid)
# maxc = max(c for r, c in grid)
#
# for r in range(0, maxr + 1):
#     for c in range(0, maxc + 1):
#         print(g[r, c], end='')
#     print()

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

assert aa == 1523
assert bb == 9290
