import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import combinations, pairwise, permutations, product

from PIL import Image, ImageDraw

DIRS = U, R, D, L = (-1, 0), (0, 1), (1, 0), (0, -1)


def neighbors4(r, c):
    for roff, coff in DIRS:
        yield r + roff, c + coff


def draw(points):
    minx = min(x for x, y in points)
    maxx = max(x for x, y in points)
    miny = min(y for x, y in points)
    maxy = max(y for x, y in points)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print(
                '#' if (x, y) in spots else ('X' if (x, y) in points else '.'),
                end=''
            )
        print()


aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

spots = [tuple(map(int, line.split(','))) for line in lines]


def area(p, q):
    xoff = abs(p[0] - q[0] + 1)
    yoff = abs(p[1] - q[1] + 1)
    return xoff * yoff


best = (float('-inf'), (0, 0), (0, 0))
for i, p in enumerate(spots):
    for q in spots[i + 1:]:
        new = (area(p, q), p, q)
        best = max(best, new)

aa = best[0]

if locals().get('aa') is not None:
    print('part1:', aa)

filled = set()

minx = min(x for x, y in spots)
maxx = max(x for x, y in spots)
miny = min(y for x, y in spots)
maxy = max(y for x, y in spots)

scale = 100

im = Image.new(
    'RGB', (
        (maxx - minx + scale) // scale + scale,
        (maxy - miny + scale) // scale + scale
    )
)
draw = ImageDraw.Draw(im)

rows = []

at_x = defaultdict(set)
at_y = defaultdict(set)

outer = set()

for p, q in pairwise(spots + spots[:1]):
    xoff = q[0] - p[0]
    yoff = q[1] - p[1]

    xstep = ystep = 0
    if xoff:
        xstep = 1 if xoff > 0 else -1
    if yoff:
        ystep = 1 if yoff > 0 else -1

    # add "outer" tiles (left of current)
    s = xstep, ystep
    xstepo = ystepo = 0
    if xstep == -1:
        ystepo = -1
    elif xstep == 1:
        ystepo = 1
    elif ystep == -1:
        xstepo = 1
    elif ystep == 1:
        xstepo = -1

    u, v = p, q

    filled |= {p, q}
    while p != q:
        filled.add(p)
        outer.add((p[0] + xstepo, p[1] + ystepo))
        p = (p[0] + xstep, p[1] + ystep)

    outer.add((u[0] + xstepo, u[1] + ystepo))
    outer.add((v[0] + xstepo, v[1] + ystepo))

    uu = ((u[0] - minx) // scale, (u[1] - miny) // scale)
    vv = ((v[0] - minx) // scale, (v[1] - miny) // scale)
    draw.line((*uu, *vv), fill=(64, 64, 64), width=1)
    draw.line((*uu, *uu), fill=(255, 0, 0), width=10)
    draw.line((*vv, *vv), fill=(255, 0, 0), width=10)

    # uu = ((u[0] - minx + xoffo) // scale, (u[1] - miny + yoffo) // scale)
    # vv = ((v[0] - minx + xoffo) // scale, (v[1] - miny + yoffo) // scale)
    # draw.line((*uu, *vv), fill=(0, 255, 0), width=1)

im.save('a.png')
print('saved')

outer -= filled

print(len(outer) - len(filled))


def contains(u, p, q):
    (xn, x1, x2), (yn, y1, y2) = zip(u, p, q)
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    r = (x1, y2)
    s = (x2, y1)

    if u in (r, s):
        return False

    return xn in range(x1 + 1, x2 + 1) and yn in range(y1 + 1, y2 + 1)


def valid_area(p, q):
    x1, y1 = p
    x2, y2 = q

    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    for x in range(x1, x2 + 1):
        if {(x, y1), (x, y2)} & outer:
            return False

    for y in range(y1, y2 + 1):
        if {(x1, y), (x2, y)} & outer:
            return False

    return True


for x, y in filled:
    at_x[x].add(y)
    at_y[y].add(x)

for x in range(minx, maxx + 1):
    if pts := at_x.get(x):
        print(x, pts)

best = float('-inf')
for p, q in combinations(spots, r=2):
    a = area(p, q)
    if a <= best:
        continue

    success = valid_area(p, q)

    if success:
        best = max(best, a)

        print(
            'candidate', a, 'success' if success else 'failed', p, q, '=>',
            best
        )

# part 2 wrong 4496928723 (too high)
# 136459862 low
# 4496928723 high

bb = best

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
