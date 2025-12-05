import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()

a, b = s.split('\n\n')

ranges = []


def inrange(i):
    for a, b in ranges:
        if i in range(a, b + 1):
            return True
    return False


for line in a.split('\n'):
    ranges.append(tuple(map(int, line.split('-'))))

aa = 0
for i in b.splitlines():
    print(i)
    aa += inrange(int(i))

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
