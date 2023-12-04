#!/usr/bin/env python3
import re
from collections import Counter
import sys


def main():
    lines = sys.stdin.read().strip().split('\n')

    # total number of each scratchcard (original + copies)
    numcards = Counter()

    ans1 = 0
    for i, line in enumerate(lines):
        line = re.sub(r'\s+', ' ', line)
        win, cards = line.split(':')[1].split(' | ')
        win = set(map(int, win.strip().split(' ')))
        cards = list(map(int, cards.strip().split(' ')))

        matches = Counter()
        for match in win & set(cards):
            matches[match] += 1

        num_matches = sum(matches.values())
        ans1 += 2**(num_matches - 1) if matches else 0

        # count the original card, then add copies of later cards based on how
        # many matches there were (also based on how many of the current card
        # we have)
        numcards[i] += 1
        for j in range(num_matches):
            numcards[i + j + 1] += numcards[i]

    ans2 = sum(numcards.values())
    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 24706
    assert ans2 == 13114317


if __name__ == '__main__':
    main()
