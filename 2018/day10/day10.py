import re
import sys


def simulate(objects):
    return [[x + vx, y + vy, vx, vy] for x, y, vx, vy in objects]


def display(objectss):
    minx = min(x for x, y, vx, vy in objects)
    miny = min(y for x, y, vx, vy in objects)
    maxx = max(x for x, y, vx, vy in objects)
    maxy = max(y for x, y, vx, vy in objects)
    points = {(x, y) for x, y, vx, vy in objects}

    print()
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print('#' if (x, y) in points else '.', end='')
        print()
    print()


objects = [list(map(int, re.findall(r'-?\d+', line))) for line in sys.stdin]


def spread_cost(objects):
    minx = min(x for x, _, _, _ in objects)
    miny = min(y for _, y, _, _ in objects)
    maxx = max(x for x, _, _, _ in objects)
    maxy = max(y for _, y, _, _ in objects)
    return maxx - minx + maxy - miny


best_cost = spread_cost(objects)
best_objects = objects
steps = 0
while best_cost > 70:
    objects = simulate(objects)
    ncost = spread_cost(objects)
    steps += 1
    if ncost < best_cost:
        best_cost = ncost
        best_objects = objects
        print('new best', ncost)

display(objects)

a1 = 'FPRBRRZA'
a2 = steps

print('part1:', a1)
print('part2:', a2)

assert a2 == 10027
