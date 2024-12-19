#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from functools import cache
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

a,b = sys.stdin.read().strip().split('\n\n')

avails = set(a.split(', '))
designs = b.split('\n')

@cache
def is_possible(s):
    if s == '':
        return True
    for a in avails:
        if s.startswith(a):
            if is_possible(s[len(a):]):
                return True
    return False

print('part1:', sum(map(is_possible, designs)))
