import sys
from collections import Counter, defaultdict
from itertools import pairwise
from typing import cast


def neighbors4(x, y):
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y - 1)
    yield (x, y + 1)


def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def explore(p: tuple[int, int]):
    '''Totally excessive and unnecessary use of BFS'''

    return {
        (x, y): manhattan_dist((x, y), p)
        for x in range(MIN_X, MAX_X + 1)
        for y in range(MIN_Y, MAX_Y + 1)
    }


def get_all_dists():
    '''Find the shortest distance to each node from each point'''
    dists = defaultdict(list)
    for i, (x, y) in enumerate(POINTS):
        distto = explore((x, y))
        for p, dist in distto.items():
            dists[p].append((dist, i))
    return dists


def part1():
    # Find the closest node to each coordinate (ignoring duplicates)
    closest = {}
    for p, items in DISTS.items():
        items.sort()
        if items[0][0] != items[1][0]:
            closest[p] = items[0][1]

    # Count the number of each type of closest node
    c = Counter(closest.values())

    # Remove nodes that extend off into infinity
    remove = set()

    for x in range(MIN_X, MAX_X + 1):
        for y in (MIN_Y, MAX_Y):
            if i := closest.get((x, y)):
                remove.add(i)

    for y in range(MIN_Y, MAX_Y + 1):
        for x in (MIN_X, MAX_X):
            if i := closest.get((x, y)):
                remove.add(i)

    for i in remove:
        del c[i]

    return c.most_common()[0][1]


def part2():
    sums = Counter()
    for p, dist_is in DISTS.items():
        sums[p] += sum(d for d, i in dist_is)
    return sum(1 for x in sums.values() if x < 10000)


POINTS = [tuple(map(int, line.split(', '))) for line in sys.stdin]
POINTS = cast(list[tuple[int, int]], POINTS)

MIN_X = min(x for x, y in POINTS)
MIN_Y = min(y for x, y in POINTS)
MAX_X = max(x for x, y in POINTS)
MAX_Y = max(y for x, y in POINTS)

DISTS = get_all_dists()

a1 = part1()
print('part1:', a1)

a2 = part2()
print('part2:', a2)

assert a1 == 3420
assert a2 == 46667
