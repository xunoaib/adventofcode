import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()

s, b = s.split('\n\n')

ranges = []


def inrange(i):
    for a, b in ranges:
        if i in range(a, b + 1):
            return True
    return False


for line in s.split('\n'):
    ranges.append(tuple(map(int, line.split('-'))))

aa = 0
for i in b.splitlines():
    aa += inrange(int(i))

ranges.sort()

fin = [ranges.pop(0)]

while ranges:
    s1, e1 = fin[-1]
    s2, e2 = ranges.pop(0)
    s = max(s2, e1)
    if s <= e2:
        if e1 == s:
            s += 1
        fin.append((s, e2))

bb = sum((e - s + 1) for s, e in fin)

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

assert aa == 756
assert bb == 355555479253787
