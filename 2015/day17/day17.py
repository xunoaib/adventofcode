import sys
from functools import cache
from itertools import combinations


def part1(goal: int):
    count = 0
    for r in range(1, len(sizes)):
        for comb in combinations(sizes, r=r):
            count += sum(comb) == goal
    return count


sizes = sorted(map(int, sys.stdin))[::-1]

# a1 = part1(25)
a1 = part1(150)
print('part1:', a1)
