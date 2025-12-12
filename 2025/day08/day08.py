import sys
from itertools import combinations
from math import prod


def dist(p, q):
    return sum((i - j)**2 for i, j in zip(p, q))


lines = sys.stdin.read().strip().split('\n')
points = [tuple(map(int, line.split(','))) for line in lines]
dists = sorted((dist(p, q), p, q) for p, q in combinations(points, r=2))
circuits = {}

N = 1000 if len(points) > 100 else 10

for i, (_, p, q) in enumerate(dists):
    points1 = circuits.get(p) or set()
    points2 = circuits.get(q) or set()
    newpoints = points1 | points2 | {p, q}
    circuits |= {r: newpoints for r in newpoints}

    if i == N - 1:
        ids = {id(v): v for v in circuits.values()}
        a1 = prod(sorted(map(len, ids.values()))[-3:])

    if len(newpoints) == len(points):
        a2 = p[0] * q[0]
        break

print('part1:', a1)
print('part2:', a2)

assert a1 == 83520
assert a2 == 1131823407
