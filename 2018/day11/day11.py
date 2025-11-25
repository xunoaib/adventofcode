from functools import cache

import numpy as np


@cache
def power_level(x, y, gsn):
    rack_id = x + 10
    p = rack_id * y
    p += gsn
    p *= rack_id
    p = ((p % 1000) - (p % 100)) // 100
    p -= 5
    return p


@cache
def region_power(x, y, gsn, size):
    if size == 1:
        return power_level(x, y, gsn)

    base_power = region_power(x, y, gsn, size - 1)

    xsum = sum(
        power_level(xx, y + size - 1, gsn) for xx in range(x, x + size - 1)
    )
    ysum = sum(
        power_level(x + size - 1, yy, gsn) for yy in range(y, y + size - 1)
    )
    corner = power_level(x + size - 1, y + size - 1, gsn)

    return base_power + xsum + ysum + corner


def part1():
    best = best_power_at_size(gsn, 3)
    return f'{best[1]},{best[2]}'


def part2():
    best = (float('-inf'), ) * 4

    for size in range(1, 300):
        sbest = best_power_at_size(gsn, size)
        best = min(best, sbest)
        if sbest == best:
            print(f'new best {best} with power {best[0]}')

    _, x, y, size = best
    return f'{x},{y},{size}'


def best_power_at_size(gsn: int, size: int):
    best = (float('-inf'), ) * 3
    for y in range(1, ROWS):
        for x in range(1, COLS):
            p = region_power(x, y, gsn, size)
            best = max(best, (p, x, y))
    return best


gsn = int(input())

ROWS = COLS = 300

COST_MATRIX = np.array(
    [[power_level(x, y, gsn) for x in range(COLS)] for y in range(ROWS)]
)

# for size in range(3, 300):
#     for y in range(1, ROWS - size):
#         for x in range(1, COLS - size):
#             t = m[y:y + size, x:x + size].flatten().sum()

a1 = part1()
print('part1:', a1)
assert a1 == '235,16'

a2 = part2()
print('part2:', a2)
assert a2 == '236,227,14'
