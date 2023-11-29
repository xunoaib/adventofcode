#!/usr/bin/env python3
import re
import sys


def expand(line):
    ans = ''
    for m in re.finditer(r'(.)\1{0,}', line):
        ans += str(m.end() - m.start()) + m.group(1)
    return ans

def main():
    line = sys.stdin.read().strip()

    for i in range(40):
        line = expand(line)

    ans1 = len(line)
    print('part1:', ans1)

    for i in range(10):
        line = expand(line)

    ans2 = len(line)
    print('part2:', ans2)

    assert ans1 == 329356
    assert ans2 == 4666278

if __name__ == '__main__':
    main()
