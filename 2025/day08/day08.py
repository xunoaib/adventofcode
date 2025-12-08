import sys
from collections import defaultdict
from math import prod


def dist(p, q):
    return sum((i - j)**2 for i, j in zip(p, q))


lines = sys.stdin.read().strip().split('\n')
points = [tuple(map(int, line.split(','))) for line in lines]

dists = []
for i, p in enumerate(points):
    for q in points[i + 1:]:
        dists.append((dist(p, q), p, q))
dists.sort()

circuits = defaultdict(set)

N = 1000 if len(points) > 100 else 10

for i, (_, p, q) in enumerate(dists):
    points1 = circuits.get(p, set())
    points2 = circuits.get(q, set())
    newpoints = points1 | points2 | {p, q}
    circuits |= {r: newpoints for r in newpoints}

    if i == N - 1:
        ids = {id(v): v for v in circuits.values()}
        aa = prod(sorted(len(v) for v in ids.values())[-3:])


    if len(newpoints) == len(points):
        bb = p[0] * q[0]
        break

print('part1:', aa)
print('part2:', bb)

assert aa == 83520
assert bb == 1131823407
