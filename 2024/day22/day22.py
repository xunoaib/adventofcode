#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, permutations, product

buyers = [int(x) for x in sys.stdin.read().strip().split('\n')]

def mix(a, secret):
    return a ^ secret

def prune(secret):
    return secret % 16777216

def next_secret(secret):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret


a = 0
for secret in buyers:
    orig = secret
    for _ in range(2000):
        secret = next_secret(secret)
    a += secret

print('part1:', a)
# print('part2:', a2)

# assert a1 == 0
# assert a2 == 0
