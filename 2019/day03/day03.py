#!/usr/bin/env python
import sys
from collections import defaultdict

OFFSETS = {
    'R': (+1, 0),
    'L': (-1, 0),
    'U': ( 0, +1),
    'D': ( 0, -1),
}

visited = {}
intersections = []

step_counts = defaultdict(dict)
stepsums = []

for wire_num, line in enumerate(sys.stdin):
    x,y = 0,0
    steps = 0

    for move in line.strip().split(','):
        xoff, yoff = OFFSETS[move[0]]
        dist = int(move[1:])

        # move the wire one unit at a time
        for i in range(dist):
            x += xoff
            y += yoff
            steps += 1

            # update step count for newly visited tiles
            if (x,y) not in step_counts[wire_num]:
                step_counts[wire_num][(x,y)] = steps

            # check for intersection with other wire
            other_wire = visited.get((x,y))
            if other_wire not in (wire_num, None):
                intersections.append((x,y))
                stepsums.append(steps + step_counts[other_wire][(x,y)])

            visited[(x,y)] = wire_num

dist = min(abs(x)+abs(y) for x,y in intersections)
print('closest intersection dist:', dist)
print('shortest intersection steps:', min(stepsums))
