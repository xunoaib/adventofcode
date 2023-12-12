#!/usr/bin/env python3
import re
import sys
from itertools import product

def isvalid(line, nums):
    return nums == [len(g) for g in re.split(r'\.+', line.strip('.'))]


def solve1(line, nums):
    chars = list(line)
    qs = [i for i, ch in enumerate(line) if ch == '?']
    count = 0
    for perm in product('.#', repeat=len(qs)):
        for i, ch in zip(qs, perm):
            chars[i] = ch
        if isvalid(''.join(chars), nums):
            count += 1
    return count


def main():
    lines = sys.stdin.read().strip().split('\n')

    ans1 = 0
    for line in lines:
        line, nums = line.split(' ')
        nums = list(map(int, nums.split(',')))
        ans1 += solve1(line, nums)

    print('part1:', ans1)

if __name__ == '__main__':
    main()
