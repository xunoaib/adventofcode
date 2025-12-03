import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import combinations, pairwise, permutations, product

aa = bb = None

lines = sys.stdin.read().strip().split('\n')

aa = 0

for line in lines:
    xs = list(map(int, list(line)))

    m = 0
    for a, b in combinations(xs, r=2):
        m = max(m, int(f'{a}{b}'))

    print(m)

    # a = max(xs)
    # i = xs.index(a)
    # xs.remove(a)
    # b = max(xs)
    # j = xs.index(b)

    # if j < i:
    #     a, b = b, a

    # print(a, b)
    aa += m

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
