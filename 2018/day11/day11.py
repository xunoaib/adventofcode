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


gsn = int(input())

# gsn = 18  # FIXME:
# print(region_power(33, 45, gsn, 3))
# exit()

ROWS = COLS = 300

best = (float('-inf'), ) * 3

for y in range(1, ROWS):
    for x in range(1, COLS):
        p = region_power(x, y, gsn, 3)
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
                print('new best', a2, best[0])

# NOTE: this answer is found quickly but the full search is very inefficient
assert a2 == '236,227,14'
