import sys
from itertools import combinations


def part1(goal: int):
    count = 0
    for r in range(1, len(sizes)):
        for comb in combinations(sizes, r=r):
            count += sum(comb) == goal
    return count


def part2(goal: int):
    for r in range(1, len(sizes)):
        count = 0
        for comb in combinations(sizes, r=r):
            count += sum(comb) == goal
        if count:
            return count


sizes = sorted(map(int, sys.stdin))[::-1]

a1 = part1(150)
a2 = part2(150)

print('part1:', a1)
print('part2:', a2)

assert a1 == 4372
assert a2 == 4
