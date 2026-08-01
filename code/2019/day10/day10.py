#!/usr/bin/env python3
import math
import sys
from collections import defaultdict

def part1(grid):
    asteroids = [(r,c) for r,row in enumerate(grid) for c,ch in enumerate(row) if ch == '#']
    return max((len(slope_lookups(grid, asteroids, r, c)), (r,c)) for r,c in asteroids)[0]

def part2(grid):
    asteroids = [(r,c) for r,row in enumerate(grid) for c,ch in enumerate(row) if ch == '#']
    base = max((len(slope_lookups(grid, asteroids, r, c)), (r,c)) for r,c in asteroids)[1]

    slope_to_asts = slope_lookups(grid, asteroids, *base)
    slope_order = sorted(list(slope_to_asts), key=lambda slope: (math.degrees(math.atan2(*slope))-90) % 360)

    count = 0
    while True:
        for slope in slope_order.copy():
            asts = slope_to_asts.get(slope)
            ast = asts.pop(0)
            count += 1
            # print(count, 'zapped', ast)
            if count == 200:
                return ast[1] * 100 + ast[0]
            if not asts:
                slope_order.remove(slope)
        if not slope_order:
            raise ValueError('zapped everything')

def find_slope(a, b):
    r = a[0] - b[0]
    c = a[1] - b[1]
    gcd = math.gcd(r, c)
    return r // gcd, c // gcd

def slope_lookups(grid, asteroids, r, c):
    """Group asteroids by their slopes relative to a single point (r,c), sorted by their distance from that point.
    result[slope] => list of asteroids that fall on this line, ordered by distance
    """
    slopes = defaultdict(list)
    for asteroid in asteroids:
        if asteroid == (r,c):
            continue
        slope = find_slope((r,c), asteroid)
        slopes[slope].append(asteroid)

    # sort asteroids based on their distance
    for slope in slopes:
        slopes[slope].sort(key=lambda ast: (ast[0]-r)**2 + (ast[1]-c)**2)
    return dict(slopes)

def main():
    grid = sys.stdin.read().split()

    ans1 = part1(grid)
    print('part1:', ans1)

    ans2 = part2(grid)
    print('part2:', ans2)

    assert ans1 == 269
    assert ans2 == 612

if __name__ == '__main__':
    main()
