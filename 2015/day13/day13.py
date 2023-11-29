#!/usr/bin/env python3
import re
import sys
from collections import defaultdict
from itertools import permutations


def total_happiness(tothap, arrangement):
    people = arrangement + (arrangement[0], )
    total = 0
    for i in range(len(people) - 1):
        p1, p2 = people[i:i + 2]
        total += tothap[p1][p2]
        total += tothap[p2][p1]
    return total

def part1(tothap):
    return max(total_happiness(tothap, perm) for perm in permutations(tothap.keys()))

def part2(tothap):
    for guest in list(tothap):
        tothap[guest]['me'] = 0
        tothap['me'][guest] = 0
    return part1(tothap)

def main():
    lines = sys.stdin.read().strip().split('\n')

    tothap = defaultdict(dict)
    for line in lines:
        m = re.match('(.*) would (.*) (.*) happiness units by sitting next to (.*).', line)
        p1, impact, amt, p2 = m.groups()
        amt = int(amt) * (-1 if impact == 'lose' else 1)
        tothap[p1][p2] = amt

    ans1 = part1(tothap)
    print('part1:', ans1)

    ans2 = part2(tothap)
    print('part2:', ans2)

    assert ans1 == 733
    assert ans2 == 725

if __name__ == '__main__':
    main()
