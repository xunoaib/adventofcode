#!/usr/bin/env python3
import sys
from functools import cache


def solve(line, nums):
    chars = list('.' + line + '.')

    @cache
    def _solve(ch=None, idx=0, nidx=0, groupsize=0):
        if idx >= len(chars):
            return int(nidx >= len(nums))

        match chars[idx]:
            case '#':
                groupsize += 1
                if nidx >= len(nums) or groupsize > nums[nidx]:
                    return 0
            case '.':
                if chars[idx - 1] == '#':
                    if groupsize != nums[nidx]:
                        return 0
                    groupsize = 0
                    nidx += 1
            case '?':
                chars[idx] = '.'
                a = _solve('.', idx, nidx, groupsize)
                chars[idx] = '#'
                b = _solve('#', idx, nidx, groupsize)
                chars[idx] = '?'
                return a + b

        return _solve(chars[idx], idx + 1, nidx, groupsize)

    return _solve()


def main():
    lines = sys.stdin.read().strip().split('\n')
    ans1 = ans2 = 0

    for line in lines:
        line, ns = line.split(' ')
        nums = list(map(int, ns.split(',')))
        ans1 += solve(line, nums)
        ans2 += solve('?'.join([line] * 5), nums * 5)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 8180
    assert ans2 == 620189727003627


if __name__ == '__main__':
    main()
