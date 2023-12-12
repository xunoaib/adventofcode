#!/usr/bin/env python3
import sys
from functools import cache

chars: list = []
nums: list = []


@cache
def solve(ch=None, idx=0, nidx=0, groupsize=0):
    if idx >= len(chars):
        return int(nidx >= len(nums))

    ch = chars[idx]
    if ch == '#':
        groupsize += 1
        if nidx >= len(nums) or groupsize > nums[nidx]:
            return 0
    elif ch == '.':
        if chars[idx - 1] == '#':
            if groupsize != nums[nidx]:
                return 0
            groupsize = 0
            nidx += 1
    elif ch == '?':
        chars[idx] = '.'
        a = solve('.', idx, nidx, groupsize)
        chars[idx] = '#'
        b = solve('#', idx, nidx, groupsize)
        chars[idx] = '?'
        return a + b

    return solve(ch, idx + 1, nidx, groupsize)


def main():
    global nums, chars
    lines = sys.stdin.read().strip().split('\n')

    ans1 = ans2 = 0
    for line in lines:
        line, ns = line.split(' ')
        nums = list(map(int, ns.split(',')))
        chars = list('.' + line + '.')
        solve.cache_clear()
        ans1 += solve()

        line = '?'.join([line] * 5)
        nums *= 5
        chars = list('.' + line + '.')
        solve.cache_clear()
        ans2 += solve()

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 8180
    assert ans2 == 620189727003627


if __name__ == '__main__':
    main()
