import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

for line in lines:
    pass

beams = {i for i, ch in enumerate(lines[0]) if ch == 'S'}
splits = 0

for line in lines:
    for i, ch in enumerate(line):
        if i in beams:
            if ch == '^':
                beams.remove(i)
                beams.add(i - 1)
                beams.add(i + 1)
                splits += 1

# print(len(beams))
aa = splits

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
