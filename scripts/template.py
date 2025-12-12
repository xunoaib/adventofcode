import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

lines = sys.stdin.read().strip().split('\n')

# s = sys.stdin.read()
# vs = list(tuple(map(int, s.split(','))))

for line in lines:
    a, b = line.split(',')

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
