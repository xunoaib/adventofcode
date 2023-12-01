#!/usr/bin/env python3
import re
import string
import sys

digitnames = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
]

namestodigit = {name: str(i + 1) for i, name in enumerate(digitnames)}


def score(line, pattern):
    found = re.findall(f'(?={pattern})', line)
    digits = ''.join([namestodigit.get(d, d) for d in found])
    return int(digits[0] + digits[-1])


def main():
    lines = sys.stdin.read().strip().lower().split('\n')

    pattern1 = '(' + r'|'.join(string.digits) + ')'
    pattern2 = '(' + r'|'.join(list(string.digits) + digitnames) + ')'

    ans1 = sum(score(line, pattern1) for line in lines)
    ans2 = sum(score(line, pattern2) for line in lines)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 55172
    assert ans2 == 54925


if __name__ == '__main__':
    main()
