#!/usr/bin/env python3
import sys

OFFSETS = [(0, 1), (-1, 0), (0, -1), (1, 0)]

def neighbors(grid, r, c):
    for roff in (-1, 0, 1):
        for coff in (-1, 0, 1):
            yield grid.get((r + roff, c + coff), 0)

def part1(goal):
    direction = r = c = idx = 0
    current = 1

    while current <= goal:
        length = idx // 2 + 1
        roff, coff = OFFSETS[direction]
        r += roff * length
        c += coff * length
        direction = (direction + 1) % 4
        current += length
        idx += 1

    # subtract overshot distance
    diff = current - goal
    roff, coff = OFFSETS[(direction-1) % 4]
    r -= roff * diff
    c -= coff * diff

    return abs(r) + abs(c)

OFFSETS = [(0, 1), (-1, 0), (0, -1), (1, 0)]

def part2(goal):
    direction = r = c = 0
    grid = {(r,c): 1}

    current = 1   # cell number counter
    nextturn = 2  # next cell number to turn left at
    interval = 2  # divide by 2 to get the current side length

    while grid[(r,c)] <= goal:
        roff, coff = OFFSETS[direction]
        r += roff
        c += coff
        grid[r,c] = sum(neighbors(grid, r, c))
        current += 1

        if current >= nextturn:
            direction = (direction + 1) % 4
            interval += 1
            nextturn += interval // 2

    return grid[(r,c)]

def print_grid():
    direction = 0
    r = c = 0

    grid = {(r,c): 1}

    current = 1   # square counter
    nextturn = 2  # when current == nextturn, turn left
    interval = 2  # divide by 2 to get the current side length

    for i in range(99):
        roff, coff = OFFSETS[direction]
        r += roff
        c += coff
        grid[r,c] = current + 1
        current += 1

        if current >= nextturn:
            direction += 1
            direction %= 4
            interval += 1
            nextturn += interval // 2

    minr = min(r for r,c in grid)
    maxr = max(r for r,c in grid)
    minc = min(c for r,c in grid)
    maxc = max(c for r,c in grid)

    for r in range(minr, maxr+1):
        for c in range(minc, maxc+1):
            print('{:>3}'.format(grid.get((r,c), '')), end='')
        print()

def main():
    goal = int(sys.stdin.read())

    ans1 = part1(goal)
    print('part1:', ans1)

    ans2 = part2(goal)
    print('part2:', ans2)

    assert ans1 == 552
    assert ans2 == 330785

if __name__ == '__main__':
    main()
