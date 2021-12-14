#!/usr/bin/env python3
import sys
from collections import Counter
from functools import cache


def replace(pattern, rules):
    s = ''
    for i in range(len(pattern) - 1):
        pair = pattern[i:i + 2]
        s += pair[0]
        if rule := rules.get(pair):
            s += rule
    return s + pair[1]

def part1(pattern, rules):
    for _ in range(10):
        pattern = replace(pattern, rules)
    counts = Counter(pattern)
    return max(counts.values()) - min(counts.values())

def part2(pattern, rules):
    @cache
    def recurse(pair, depth=0):
        """Returns the number of occurrences of each character after 'depth' iterations"""
        if depth == 0:
            return Counter(pair)

        if char := rules.get(pair):
            left = recurse(pair[0] + char, depth - 1)
            right = recurse(char + pair[1], depth - 1)
            res = {k: left.get(k, 0) + right.get(k, 0) for k in set(left) | set(right)}
            res[char] -= 1
            return res
        return Counter(pair)

    # split large string into character pairs and gather character counts for each
    counts = Counter()
    for i in range(len(pattern) - 1):
        pair = pattern[i:i + 2]
        subcounts = recurse(pair, 40)
        for k, v in subcounts.items():
            counts[k] += v

    # subtract inner characters from the final count, as they get counted twice above
    for ch in pattern[1:-1]:
        counts[ch] -= 1

    return max(counts.values()) - min(counts.values())

def main():
    pattern = sys.stdin.readline().strip()
    rules = dict(line.split(' -> ') for line in sys.stdin.read().strip().split('\n'))

    ans1 = part1(pattern, rules)
    print('part1:', ans1)

    ans2 = part2(pattern, rules)
    print('part2:', ans2)

    assert ans1 == 5656
    assert ans2 == 12271437788530

if __name__ == '__main__':
    main()
