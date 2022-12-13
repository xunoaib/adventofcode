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
            if (res := compare(a, b)) is not None:
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


def cmp(left, right):
    result = compare(left, right)
    return [True, None, False].index(result) - 1


def main():
    groups = sys.stdin.read().strip().split('\n\n')
    pairs = [list(map(json.loads, group.split('\n'))) for group in groups]

    ans1 = 0
    for i, (a, b) in enumerate(pairs):
        if compare(a, b):
            ans1 += i + 1

    print('part1:', ans1)

    flattened = [item for sublist in pairs for item in sublist]
    flattened += [[[2]], [[6]]]
    flattened.sort(key=cmp_to_key(cmp))

    p1 = flattened.index([[2]]) + 1
    p2 = flattened.index([[6]]) + 1
    ans2 = p1 * p2
    print('part2:', ans2)

    assert ans1 == 6072
    assert ans2 == 22184


if __name__ == '__main__':
    main()
