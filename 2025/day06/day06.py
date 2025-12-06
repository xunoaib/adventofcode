import re
import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

aa = bb = None

s = sys.stdin.read()
lines = s.strip().split('\n')

*nums, ops = [re.split(r'\s+', line.strip()) for line in lines]

nums = [list(map(int, row)) for row in nums]
print(nums)

aa = 0

for a, b, c, d, o in zip(*nums, ops):
    aa += eval(f'{a}{o}{b}{o}{c}{o}{d}')

if locals().get('aa') is not None:
    print('part1:', aa)

if locals().get('bb') is not None:
    print('part2:', bb)

# assert aa == 0
# assert bb == 0
