import re
import sys


def simulate(objects):
    return [[x + vx, y + vy, vx, vy] for x, y, vx, vy in objects]


def display():
    minx = min(x for x, y, vx, vy in objects)
    miny = min(y for x, y, vx, vy in objects)
    maxx = max(x for x, y, vx, vy in objects)
    maxy = max(y for x, y, vx, vy in objects)
    points = {(x, y) for x, y, vx, vy in objects}

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            print('#' if (x, y) in points else '.', end='')
        print()

    print()


objects = []
for line in sys.stdin:
    obj = px, py, vx, vy = list(map(int, re.findall(r'-?\d+', line)))
    objects.append(obj)

display()
objects = simulate(objects)
display()
objects = simulate(objects)
display()
objects = simulate(objects)
display()
