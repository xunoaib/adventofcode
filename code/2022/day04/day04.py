#!/usr/bin/env python3
import re
import sys

# comparing the start and end ranges is more efficient, but set operations require less thinking :)

def main():
    lines = sys.stdin.read().strip().split('\n')

    ans1 = 0
    for line in lines:
        a, b, c, d = map(int, re.split(r'[-,]', line))
        x = set(range(a, b + 1))
        y = set(range(c, d + 1))

        if x.issubset(y) or y.issubset(x):
            ans1 += 1

    print('part1:', ans1)

    ans2 = 0
    for line in lines:
        a, b, c, d = map(int, re.split(r'[-,]', line))
        x = set(range(a, b + 1))
        y = set(range(c, d + 1))

        if x & y:
            ans2 += 1

    print('part2:', ans2)

    assert ans1 == 595
    assert ans2 == 952


if __name__ == '__main__':
    main()
