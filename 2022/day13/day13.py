#!/usr/bin/env python3
import json
import sys
from functools import cmp_to_key


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right
    elif isinstance(left, list) and isinstance(right, list):
        for a, b in zip(left, right):
            res = compare(a, b)
            if res is not None:
                return res
        if len(left) == len(right):
            return None
        return len(left) < len(right)
    else:
        if isinstance(left, int):
            left = [left]
        elif isinstance(right, int):
            right = [right]
        return compare(left, right)


def make_comparator(less_than):

    def compare(x, y):
        if less_than(x, y):
            return -1
        elif less_than(y, x):
            return 1
        else:
            return 0

    return compare


def main():
    groups = sys.stdin.read().strip().split('\n\n')
    pairs = [
        list(json.loads(line) for line in group.split('\n')) for group in groups
    ]

    ans1 = 0
    for i, (a, b) in enumerate(pairs):
        if compare(a, b):
            ans1 += i + 1

    print('part1:', ans1)

    pairs.append([[[2]], [[6]]])
    flattened = [item for sublist in pairs for item in sublist]
    sorted_pairs = sorted(flattened, key=cmp_to_key(make_comparator(compare)))

    p1 = sorted_pairs.index([[2]]) + 1
    p2 = sorted_pairs.index([[6]]) + 1
    ans2 = p1 * p2
    print('part2:', ans2)

    assert ans1 == 6072
    assert ans2 == 22184


if __name__ == '__main__':
    main()
