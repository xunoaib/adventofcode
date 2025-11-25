import numpy as np


def power_level(x, y):
    rack_id = x + 10
    p = ((rack_id * y) + GSN) * rack_id
    return ((p % 1000) - (p % 100)) // 100 - 5


def part1():
    best = best_power_at_size(3)
    return f'{best[1]},{best[2]}'


def part2():
    best = (float('-inf'), ) * 4

    for size in range(1, 300):
        sbest = best_power_at_size(size)
        best = max(best, sbest)
        if sbest == best:
            print(f'new best {best} with power {best[0]}')

    _, x, y, size = best
    return f'{x},{y},{size}'


def best_power_at_size(size: int):
    best = (float('-inf'), ) * 4
    for y in range(1, ROWS - size):
        for x in range(1, COLS - size):
            p = COST_MATRIX[y:y + size, x:x + size].flatten().sum()
            best = max(best, (p, x, y, size))
    return best


GSN = int(input())

ROWS = COLS = 300

COST_MATRIX = np.array(
    [[power_level(x, y) for x in range(COLS)] for y in range(ROWS)]
)

a1 = part1()
print('part1:', a1)
assert a1 == '235,16'

a2 = part2()
print('part2:', a2)
assert a2 == '236,227,14'
