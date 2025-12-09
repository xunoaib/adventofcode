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

import pandas as pd

rows = []

at_x = defaultdict(set)
at_y = defaultdict(set)

for p, q in pairwise(spots + spots[:1]):
    xoff = q[0] - p[0]
    yoff = q[1] - p[1]

    # print(xoff, yoff)

    xstep = ystep = 0
    if xoff:
        xstep = 1 if xoff > 0 else -1
    if yoff:
        ystep = 1 if yoff > 0 else -1

    u, v = p, q

    filled |= {p, q}
    while p != q:
        filled.add(p)
        p = (p[0] + xstep, p[1] + ystep)

    u = ((u[0] - minx) // scale, (u[1] - miny) // scale)
    v = ((v[0] - minx) // scale, (v[1] - miny) // scale)
    draw.line((*u, *v), fill=(255, 255, 255), width=1)
    rows.append((xoff, yoff))

df = pd.DataFrame(rows, columns=['xoff', 'yoff'])
# print(df['xoff'].value_counts().to_dict())

# print(maxx - minx, maxy - miny)


def contains(u, p, q):
    ''' If p+q contains u '''
    (xn, x1, x2), (yn, y1, y2) = zip(u, p, q)
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    r = (x1, y2)
    s = (x2, y1)

    if u in (r, s):
        return False

    # return xn in range(x1, x2 + 1) and yn in range(y1, y2 + 1)
    # return xn in range(x1 + 1, x2) and yn in range(y1 + 1, y2)
    return xn in range(x1 + 1, x2 + 1) and yn in range(y1 + 1, y2 + 1)


best = float('-inf')
for p, q in combinations(spots, r=2):
    a = area(p, q)
    if a > best:
        success = not any(contains(u, p, q) for u in spots if u not in (p, q))

        if success:
            best = max(best, a)

        print(
            'candidate', a, 'success' if success else 'failed', p, q, '=>',
            best
        )

# for x, y in filled:
#     at_x[x].add(y)
#     at_y[y].add(x)

# for x in range(minx, maxx + 1):
#     if pts := at_x.get(x):
#         print(x, pts)

# part 2 wrong 4496928723 (too high)

bb = best

im.save('a.png')
print('saved')

# print(len(filled))
#
# seen = set()
#
# print('---')
#
# p = spots[0] if len(spots) < 100 else spots[1]
#
# q = [(p[0] + 2, p[1] + 2)]
# seen = {q[0]}
# while q:
#     p = q.pop()
#
#     x, y = p
#     if x not in range(minx, maxx + 1) or y not in range(miny, maxy + 1):
#         print('oob')
#         exit()
#
#     for n in neighbors4(*p):
#         if n not in filled and n not in seen:
#             seen.add(n)
#             q.append(n)
#
# print(len(seen))

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
