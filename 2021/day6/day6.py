#!/usr/bin/env python3
import sys
from collections import defaultdict

def run_day(old_counts):
    counts = defaultdict(lambda: 0)
    for val, count in list(old_counts.items()):
        if val == 0:
            counts[6] += count
            counts[8] += count
        else:
            counts[val - 1] += count
    return dict(counts)

def run_days(counts, num_days):
    for _ in range(num_days):
        counts = run_day(counts)
    return sum(counts.values())

def main():
    fishes = list(map(int, sys.stdin.read().split(',')))
    counts = {val: fishes.count(val) for val in set(fishes)}

    ans1 = run_days(counts, 80)
    ans2 = run_days(counts, 256)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 386536
    assert ans2 == 1732821262171

if __name__ == '__main__':
    main()
