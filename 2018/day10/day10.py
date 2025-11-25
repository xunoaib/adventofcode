import re
import sys


def simulate(objects: list[list[int]]):
    return [[x + vx, y + vy, vx, vy] for x, y, vx, vy in objects]


def display(objects: list[list[int]]):
    minx = min(x for x, _, _, _ in objects)
    miny = min(y for _, y, _, _ in objects)
    maxx = max(x for x, _, _, _ in objects)
    maxy = max(y for _, y, _, _ in objects)
    points = {(x, y) for x, y, _, _ in objects}

    print()
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print('#' if (x, y) in points else '.', end='')
        print()
    print()


def spread_cost(objects: list[list[int]]):
    minx = min(x for x, _, _, _ in objects)
    miny = min(y for _, y, _, _ in objects)
    maxx = max(x for x, _, _, _ in objects)
    maxy = max(y for _, y, _, _ in objects)
    return maxx - minx + maxy - miny


objects = [list(map(int, re.findall(r'-?\d+', line))) for line in sys.stdin]

best = float('inf')
step = 0

while True:
    nobjects = simulate(objects)
    ncost = spread_cost(nobjects)

    if ncost > best:
        break

    step += 1
    objects = nobjects
    best = ncost

display(objects)

a1 = 'FPRBRRZA'
a2 = step

print('part1:', a1)
print('part2:', a2)

assert a2 == 10027
