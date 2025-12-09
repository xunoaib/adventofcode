import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

spots = [tuple(map(int, line.split(','))) for line in lines]

print(spots)

# grid = {
#     (r, c): ch
#     for r, line in enumerate(lines)
#     for c, ch in enumerate(line)
# }


def dist(p, q):
    # return sum(abs(i - j) for i, j in zip(p, q))
    # return p[0]*q[0], p[1]*q[1]
    xoff = abs(p[0] - q[0] + 1)
    yoff = abs(p[1] - q[1] + 1)
    return xoff * yoff


best = (float('-inf'), (0, 0), (0, 0))

for i, p in enumerate(spots):
    for q in spots[i + 1:]:
        new = (dist(p, q), p, q)
        if new >= best:
            print(new)
        best = max(best, new)

print(best)

aa = best[0]

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0

# wrong 4746376273
