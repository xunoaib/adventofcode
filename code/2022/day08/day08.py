#!/usr/bin/env python3
import itertools
import sys


def rotate(grid):
    return [list(x) for x in list(zip(*grid[::-1]))]


def scenic_score(grid, r, c, direction=None, height=None):
    if direction is None:
        mul = 1
        for d in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            mul *= scenic_score(grid, r + d[0], c + d[1], d, grid[r][c])
        return mul

    dr, dc = direction
    if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
        if grid[r][c] < height:
            return 1 + scenic_score(grid, r + dr, c + dc, direction, height)
        return 1
    return 0


def main():
    lines = sys.stdin.read().strip().split('\n')
    nums = [list(map(int, line)) for line in lines]
    visible = [[False] * len(line) for line in lines]  # tracks which trees in 'nums' are visible

    # rotate 4 times so we can use the same algo to check tree visibility from each side
    for _ in range(4):
        for r, row in enumerate(nums):
            tallest = -1
            for c, height in enumerate(row):
                if height > tallest:
                    tallest = height
                    visible[r][c] = True
        nums = rotate(nums)
        visible = rotate(visible)

    ans1 = sum(row.count(True) for row in visible)
    print('part1:', ans1)

    ans2 = max(scenic_score(nums, r, c) for r, c in itertools.product(range(len(nums)), range(len(nums[0]))))
    print('part2:', ans2)

    assert ans1 == 1825
    assert ans2 == 235200


if __name__ == '__main__':
    main()
