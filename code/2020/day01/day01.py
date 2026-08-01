#!/usr/bin/env python
import sys
import math
from itertools import combinations

nums = sorted(int(v) for v in sys.stdin)

for comb in combinations(nums, 2):
    if sum(comb) == 2020:
        print('part1: ', math.prod(comb))

for comb in combinations(nums, 3):
    if sum(comb) == 2020:
        print('part2: ', math.prod(comb))
