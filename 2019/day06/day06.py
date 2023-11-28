#!/usr/bin/env python3
import sys
from collections import defaultdict

def part1(orbits):
    return sum(count_orbits(orbits, obj) for obj in orbits)

def count_orbits(orbits, obj):
    if orbits[obj]:
        return 1 + count_orbits(orbits, orbits[obj])
    return 0

def part2(orbits, t1='YOU', t2='SAN'):
    """Find the minimum number of jumps to get from t1 to t2"""
    # trace t1 to root, counting the number of jumps for each node
    costs = {t1: 0}
    parent = t1
    while child := orbits[parent]:
        costs[child] = costs[parent] + 1
        parent = child

    # trace t2 to root, counting jumps until a shared ancestor of t1 is found
    t2_cost = 0
    parent = t2
    while child := orbits[parent]:
        if cost := costs.get(child):
            return t2_cost + cost - 1
        t2_cost += 1
        parent = child

def main():
    orbits = defaultdict(lambda: None)
    for line in sys.stdin:
        child, parent = line.strip().split(')')
        orbits[parent] = child
        orbits[child]
    orbits = dict(orbits)

    ans1 = part1(orbits)
    print('part1:', ans1)

    ans2 = part2(orbits)
    print('part2:', ans2)

    assert ans1 == 154386
    assert ans2 == 346

if __name__ == '__main__':
    main()
