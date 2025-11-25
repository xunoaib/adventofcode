from functools import cache


@cache
def power_level(x, y, gsn):
    rack_id = x + 10
    p = rack_id * y
    p += gsn
    p *= rack_id
    p = ((p % 1000) - (p % 100)) // 100
    p -= 5
    return p


def region_power(x, y, gsn, size=3):
    tot = 0
    for xoff in range(size):
        for yoff in range(size):
            tot += power_level(x + xoff, y + yoff, gsn)
    return tot


gsn = int(input())
best = (float('-inf'), ) * 3

ROWS = COLS = 300

for y in range(1, ROWS):
    for x in range(1, COLS):
        p = region_power(x, y, gsn)
        best = max(best, (p, x, y))

p, x, y = best
a1 = f'{x},{y}'
print('part1:', a1)

assert a1 == '235,16'

best = (float('-inf'), ) * 4
a2 = None

for size in range(3, 300):
    for y in range(1, ROWS - size):
        for x in range(1, COLS - size):
            p = region_power(x, y, gsn, size)
            if p > best[0]:
                best = (p, x, y, size)
                a2 = f'{x},{y},{size}'
                print('new best', best, a2)

# NOTE: this answer is found quickly but the full search is very inefficient
assert a2 == '236,227,14'
