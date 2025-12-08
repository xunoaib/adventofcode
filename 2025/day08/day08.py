import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product
from math import prod


def dist(p, q):
    return sum(abs(i - j)**2 for i, j in zip(p, q))


aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

rows = []
for line in lines:
    rows.append(tuple(map(int, line.split(','))))

distmap = {}
dists = []
for i, p in enumerate(rows):
    for j, q in enumerate(rows):
        if i < j:
            dists.append((dist(p, q), p, q))
dists.sort(reverse=True)

circuit_points = defaultdict(set)  # point => set(connected_points)

n = 1000 if len(rows) > 100 else 10

for _ in range(n):
    d, p, q = dists.pop()

    points1 = circuit_points.get(p, set())
    points2 = circuit_points.get(q, set())

    newpoints = points1 | points2 | {p, q}

    for r in newpoints:
        if r in circuit_points:
            del circuit_points[r]

    for r in newpoints:
        circuit_points[r] = newpoints

ids = {id(v): v for v in circuit_points.values()}

for i, v in ids.items():
    print(i, len(v))

sizes = sorted([len(v) for v in ids.values()])[-3:]
print(sizes)
aa = prod(sizes)

# for k, v in circuit_points.items():
#     i = id(v)
#     if i in ids:
#     print(k, len(v), )

# while dists:
#

# grid = {
#     (r, c): ch
#     for r, line in enumerate(lines)
#     for c, ch in enumerate(line)
# }

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
