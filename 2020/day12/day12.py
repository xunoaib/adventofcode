#!/usr/bin/env python
import sys

EAST, SOUTH, WEST, NORTH = range(4)

def rotate(wx, wy, num_times, clockwise):
    for i in range(num_times):
        if clockwise:
            wx, wy = wy, -wx
        else:
            wx, wy = -wy, wx
    return wx, wy

lines = [(line[0], int(line[1:])) for line in sys.stdin]

# part 1
x, y = 0, 0
direction = EAST

for cmd, num in lines:
    if cmd == 'F':
        cmd = 'ESWN'[direction]
    if cmd == 'N':
        y += num
    elif cmd == 'S':
        y -= num
    elif cmd == 'E':
        x += num
    elif cmd == 'W':
        x -= num
    elif cmd == 'L':
        direction -= num // 90
    elif cmd == 'R':
        direction += num // 90
    direction %= 4

print('part1:', abs(x) + abs(y))

# part 2
x, y = 0, 0
wx, wy = 10, 1

for cmd, num in lines:
    if cmd == 'N':
        wy += num
    elif cmd == 'S':
        wy -= num
    elif cmd == 'E':
        wx += num
    elif cmd == 'W':
        wx -= num
    elif cmd == 'F':
        x += wx * num
        y += wy * num
    else:
        wx, wy = rotate(wx, wy, num // 90, 'L' in cmd)

print('part2:', abs(x) + abs(y))
