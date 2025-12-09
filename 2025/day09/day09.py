import sys
from collections import defaultdict
from itertools import combinations, pairwise

U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def area(p, q):
    xoff = abs(p[0] - q[0]) + 1
    yoff = abs(p[1] - q[1]) + 1
    return xoff * yoff


def valid_region(p, q):
    x1, y1 = p
    x2, y2 = q

    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    for x in [x1, x2]:
        for y in at_x[x]:
            if y in range(y1, y2 + 1):
                return False

    for y in [y1, y2]:
        for x in at_y[y]:
            if x in range(x1, x2 + 1):
                return False

    return True


lines = sys.stdin.read().strip().split('\n')
corners = [tuple(map(int, line.split(','))) for line in lines]

aa = float('-inf')
for i, p in enumerate(corners):
    for q in corners[i + 1:]:
        aa = max(aa, area(p, q))

print('part1:', aa)

path = set()
outer = set()

for p, q in pairwise(corners + corners[:1]):
    xoff = q[0] - p[0]
    yoff = q[1] - p[1]

    xstep = (xoff > 0) - (xoff < 0)
    ystep = (yoff > 0) - (yoff < 0)
    xstep_out, ystep_out = {L: U, R: D, U: R, D: L}[xstep, ystep]

    pp, qq = p, q
    path |= {p, q}
    while pp != qq:
        path.add(pp)
        outer.add((pp[0] + xstep_out, pp[1] + ystep_out))
        pp = (pp[0] + xstep, pp[1] + ystep)

    outer.add((pp[0] + xstep_out, pp[1] + ystep_out))
    outer.add((qq[0] + xstep_out, qq[1] + ystep_out))

outer -= path

at_x = defaultdict(set)
at_y = defaultdict(set)
for x, y in outer:
    at_x[x].add(y)
    at_y[y].add(x)

bb = float('-inf')
for p, q in combinations(corners, r=2):
    a = area(p, q)
    if a > bb and valid_region(p, q):
        bb = a

print('part2:', bb)

assert aa == 4750176210
assert bb == 1574684850
