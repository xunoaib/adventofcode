import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import combinations, pairwise, permutations, product

aa = bb = None

lines = sys.stdin.read().strip().split('\n')

aa = bb = 0

for line in lines:
    xs = list(map(int, list(line)))

    m = 0
    for a, b in combinations(xs, r=2):
        m = max(m, int(f'{a}{b}'))

    aa += m

for line in lines:
    xs = list(map(int, list(line)))

    m = 0
    for p in combinations(range(12), r=3):
        s = ''.join(str(v) for i, v in enumerate(xs) if i not in p)
        new = int(s)
        m = max(m, new)
    bb += m

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 3121910778619
