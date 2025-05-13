#!/usr/bin/env python3
import sys
from collections import Counter
from itertools import combinations

lines = sys.stdin.read().strip().split('\n')


def part1():
    count2 = count3 = 0
    for line in lines:
        freq = Counter(line)
        count2 += 2 in freq.values()
        count3 += 3 in freq.values()
    return count2 * count3


def part2():
    for a, b in combinations(lines, r=2):
        if sum(x != y for x, y in zip(a, b)) == 1:
            return ''.join(x for x, y in zip(a, b) if x == y)


p1 = part1()
p2 = part2()

print('part1:', p1)
print('part2:', p2)

assert p1 == 8820
assert p2 == 'bpacnmglhizqygfsjixtkwudr'
