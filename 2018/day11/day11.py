def power_level(x, y, gsn):
    rack_id = x + 10
    p = rack_id * y
    p += gsn
    p *= rack_id
    p = ((p % 1000) - (p % 100)) // 100
    p -= 5
    return p


def region_power(x, y, gsn):
    tot = 0
    for xoff in range(3):
        for yoff in range(3):
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
