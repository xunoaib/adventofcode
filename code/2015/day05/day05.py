#!/usr/bin/env python3
import re
import sys

def isnice(s):
    return all([
        len(re.findall('[aeiou]', s)) >= 3,
        re.search(r'(.)\1{1,}', s),
        not re.search('ab|cd|pq|xy', s),
    ])

def isnice2(s):
    return all([
        re.search(r'(..).*\1', s),
        re.search(r'(.).\1', s)
    ])

def main():
    lines = sys.stdin.read().split()

    ans1 = sum(map(isnice, lines))
    print('part1:', ans1)

    ans2 = sum(map(isnice2, lines))
    print('part2:', ans2)

    assert ans1 == 255
    assert ans2 == 55

if __name__ == '__main__':
    main()
