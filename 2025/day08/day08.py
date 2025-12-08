import sys
from collections import defaultdict
from math import prod


def dist(p, q):
    return sum(abs(i - j)**2 for i, j in zip(p, q))


def part1(dists):
    circuit_points = defaultdict(set)

    for _ in range(N):
        _, p, q = dists.pop()

        points1 = circuit_points.get(p, set())
        points2 = circuit_points.get(q, set())
        newpoints = points1 | points2 | {p, q}

        for r in newpoints:
            if r in circuit_points:
                del circuit_points[r]

        for r in newpoints:
            circuit_points[r] = newpoints

    ids = {id(v): v for v in circuit_points.values()}
    sizes = sorted(len(v) for v in ids.values())[-3:]
    return prod(sizes)


def part2(dists):
    circuit_points = defaultdict(set)

    while True:
        _, p, q = dists.pop()

        points1 = circuit_points.get(p, set())
        points2 = circuit_points.get(q, set())
        newpoints = points1 | points2 | {p, q}

        for r in newpoints:
            if r in circuit_points:
                del circuit_points[r]

        for r in newpoints:
            circuit_points[r] = newpoints

        if len(newpoints) == len(points):
            return p[0] * q[0]


lines = sys.stdin.read().strip().split('\n')
points = [tuple(map(int, line.split(','))) for line in lines]

dists = []
for i, p in enumerate(points):
    for q in points[i + 1:]:
        dists.append((dist(p, q), p, q))

dists.sort(reverse=True)

N = 1000 if len(points) > 100 else 10

aa = part1(dists.copy())
bb = part2(dists.copy())

print('part1:', aa)
print('part2:', bb)

assert aa == 83520
assert bb == 1131823407
