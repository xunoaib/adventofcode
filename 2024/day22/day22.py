#!/usr/bin/env python3

import sys
from collections import Counter, defaultdict
from itertools import pairwise


def mix(value, secret):
    return value ^ secret

def prune(secret):
    return secret % 16777216

def next_secret(secret):
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret

secrets = list(map(int, sys.stdin))

a1 = 0
secret_prices = {}
for secret in secrets:
    orig = secret
    secret_prices[orig] = [secret % 10]
    for _ in range(2000):
        secret = next_secret(secret)
        secret_prices[orig].append(secret % 10)
    a1 += secret

print('part1:', a1)

secret_diffs = defaultdict(list)

for secret, prices in secret_prices.items():
    for a,b in pairwise(prices):
        secret_diffs[secret].append(b - a)

combined = Counter()

for secret, diffs in secret_diffs.items():
    seen = set()
    for i in range(len(diffs)-3):
        s = tuple(diffs[i:i+4])
        if s not in seen:
            seen.add(s)
            combined[s] += secret_prices[secret][i+4]

a2 = max(combined.values())

print('part2:', a2)

assert a1 == 14726157693
assert a2 == 1614
