#!/usr/bin/env python3
import sys
from collections import Counter
from functools import cache

def count_letters(pattern, rules, depth):
    @cache
    def recurse(pair, depth=0):
        """Returns the number of occurrences of each character after 'depth' iterations"""
        if depth == 0:
            return Counter(pair)

        if char := rules.get(pair):
            left = recurse(pair[0] + char, depth - 1)
            right = recurse(char + pair[1], depth - 1)
            count = left + right
            count[char] -= 1
            return count
        return Counter(pair)

    # split large string into character pairs and gather character counts for each
    counts = Counter()
    for i in range(len(pattern) - 1):
        subcounts = recurse(pattern[i:i + 2], depth)
        for k, v in subcounts.items():
            counts[k] += v

    # subtract inner characters from the final count, as they get counted twice above
    for ch in pattern[1:-1]:
        counts[ch] -= 1

    return max(counts.values()) - min(counts.values())

def main():
    pattern = sys.stdin.readline().strip()
    rules = dict(line.split(' -> ') for line in sys.stdin.read().strip().split('\n'))

    ans1 = count_letters(pattern, rules, 10)
    print('part1:', ans1)

    ans2 = count_letters(pattern, rules, 40)
    print('part2:', ans2)

    assert ans1 == 5656
    assert ans2 == 12271437788530

if __name__ == '__main__':
    main()
