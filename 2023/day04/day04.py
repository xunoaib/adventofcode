#!/usr/bin/env python3
import re
import sys
from collections import Counter


def main():
    data = sys.stdin.read().replace('  ', ' ')
    groups = re.findall(r'Card .*?: (.*?) \| (.*)', data)
    numcards = Counter()
    ans1 = 0

    for c, group in enumerate(groups):
        wins, cards = [set(map(int, s.strip().split(' '))) for s in group]

        matches = Counter()
        for m in wins & cards:
            matches[m] += 1

        if num_matches := sum(matches.values()):
            ans1 += 2**(num_matches - 1)

        numcards[c] += 1
        for i in range(num_matches):
            numcards[c + i + 1] += numcards[c]

    ans2 = sum(numcards.values())
    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 24706
    assert ans2 == 13114317


if __name__ == '__main__':
    main()
