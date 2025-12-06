import re
import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import batched, pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')


def part1():
    *nums, ops = [re.split(r'\s+', line.strip()) for line in lines]

    nums = [list(map(int, row)) for row in nums]
    print(nums)

    aa = 0

    for a, b, c, d, o in zip(*nums, ops):
        aa += eval(f'{a}{o}{b}{o}{c}{o}{d}')
    return aa


# aa = part1()

maxlen = max(len(line) for line in lines)

*nums, ops = [re.split(r'\s+', line.strip()) for line in lines]
bb = 0

outs = []
for c in range(0, maxlen):
    s = ''
    for r, row in enumerate(nums):
        s += lines[r][c]
    s = s.strip()
    outs.append(s)

if outs[-1] != '':
    outs.append('')

opidx = 0
buf = []

while outs:
    v = outs.pop(0)
    if v:
        buf.append(v)
    else:
        bb += eval(ops[opidx].join(buf))
        print(buf)
        opidx += 1
        buf = []

print(outs)

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
