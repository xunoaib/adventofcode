import re
import sys

# position=< 20247,  40241> velocity=<-2, -4>


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


objects = []
for line in sys.stdin:
    obj = px, py, vx, vy = list(map(int, re.findall(r'-?\d+', line)))
    objects.append(obj)

display()
