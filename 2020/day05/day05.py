#!/usr/bin/env python
import sys
import math

def parse_pass(line):
    rowmin, rowmax = 0, 127
    colmin, colmax = 0, 7
    for c in line.strip():
        if c == 'F':
            rowmax = int(rowmax - (rowmax - rowmin) / 2)
        elif c == 'B':
            rowmin = math.ceil(rowmin + (rowmax - rowmin) / 2)
        elif c == 'L':
            colmax = int(colmax - (colmax - colmin) / 2)
        elif c == 'R':
            colmin = math.ceil(colmin + (colmax - colmin) / 2)
        else:
            print('invalid:', c)

    assert rowmin == rowmax and colmin == colmax
    return rowmin, colmin

sids = []
for line in sys.stdin:
    row, col = parse_pass(line)
    sid = row * 8 + col
    sids.append(sid)
sids.sort()

print('part1 max:', sids[-1])

# part 2
for i in range(len(sids)-1):
    if sids[i+1] - sids[i] == 2:
        print('part2 sid:', sids[i]+1)
