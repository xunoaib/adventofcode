import sys
from collections import Counter, defaultdict
from copy import deepcopy
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

beams = {i for i, ch in enumerate(lines[0]) if ch == 'S'}
aa = 0

for line in lines:
    for i, ch in enumerate(line):
        if i in beams:
            if ch == '^':
                beams.remove(i)
                beams.add(i - 1)
                beams.add(i + 1)
                aa += 1

if locals().get('aa') is not None:
    print('part1:', aa)

beams = Counter(i for i, ch in enumerate(lines[0]) if ch == 'S')
bb = 1
for line in lines:
    newbeams = deepcopy(beams)
    print(newbeams)
    for i, ch in enumerate(line):
        if ch == '^':
            if count := beams.get(i):
                print('splitting', i)
                newbeams[i] -= count
                newbeams[i - 1] += count
                newbeams[i + 1] += count
                bb += count
    beams = newbeams

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
