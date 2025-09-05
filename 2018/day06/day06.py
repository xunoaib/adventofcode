import sys
from collections import defaultdict
from itertools import pairwise
from typing import cast


def neighbors4(x, y):
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y - 1)
    yield (x, y + 1)


def explore(p: tuple[int, int]):
    q = [(p, 0)]
    distto = {p: 0}
    while q:
        p, dist = q.pop(0)
        for n in neighbors4(*p):
            if n[0] not in range(min_x, max_x
                                 + 1) or n[1] not in range(min_y, max_y + 1):
                continue
            if n not in distto:
                distto[n] = dist + 1
                q.append((n, dist + 1))
    return distto


points = [tuple(map(int, line.split(', '))) for line in sys.stdin]
points = cast(list[tuple[int, int]], points)

min_x = min(x for x, y in points)
min_y = min(y for x, y in points)
max_x = max(x for x, y in points)
max_y = max(y for x, y in points)

dists = defaultdict(list)

for i, (x, y) in enumerate(points):
    distto = explore((x, y))

    for p, dist in distto.items():
        dists[p].append((dist, i))

    # print(len(distto))
    # dists.append(distto)

# Find the closest node to each coordinate (ignoring duplicates)
closest = {}
for p, items in dists.items():
    items.sort()
    if items[0][0] != items[1][0]:
        closest[p] = items[0][1]

p = 1, 4
p = 1, 1
# p = 1, 2

print(dists[p])
print(closest[p])
