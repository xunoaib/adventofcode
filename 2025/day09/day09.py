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

    # check for outside intersections
    for x in [x1, x2]:
        for y in outer_y_at_x[x]:
            if y1 <= y <= y2:
                return False

    for y in [y1, y2]:
        for x in outer_x_at_y[y]:
            if x1 <= x <= x2:
                return False

    return True


lines = sys.stdin.read().strip().split('\n')
corners = [tuple(map(int, line.split(','))) for line in lines]

a1 = max(area(p, q) for p, q in combinations(corners, r=2))
print('part1:', a1)

perim = set()  # tiles walked along perimeter
outer = set()  # tiles immediately outside polygon

for p, q in pairwise(corners + corners[:1]):
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    xstep = (dx > 0) - (dx < 0)
    ystep = (dy > 0) - (dy < 0)

    # vector exiting polygon
    out = {L: U, R: D, U: R, D: L}[xstep, ystep]

    cur = p
    while cur != q:
        perim.add(cur)
        outer.add((cur[0] + out[0], cur[1] + out[1]))
        cur = (cur[0] + xstep, cur[1] + ystep)

outer -= perim

# associate x => {y coords in outer region}
# for faster out-of-bounds checks
outer_y_at_x = defaultdict(set)
outer_x_at_y = defaultdict(set)

for x, y in outer:
    outer_y_at_x[x].add(y)
    outer_x_at_y[y].add(x)

a2 = float('-inf')
for p, q in combinations(corners, r=2):
    a = area(p, q)
    if a > a2 and valid_region(p, q):
        a2 = a

print('part2:', a2)

assert a1 == 4750176210
assert a2 == 1574684850
