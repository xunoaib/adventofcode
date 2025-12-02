import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None


def valid(s: str):
    for i in range(1, len(s)):
        n = len(s) // i
        if n == 2 and s[:i] * n == s:
            return False
    return True


aa = 0

for g in sys.stdin.read().split(','):
    a, b = map(int, g.split('-'))

    for i in range(a, b + 1):
        if not valid(str(i)):
            print('invalid', i)
            aa += i

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
