#!/usr/bin/env python
import sys
from collections import defaultdict

E, W, NE, NW, SE, SW = list('ewabcd')
BLACK, WHITE = 0,1

offsets = {
    E: (1,0),
    W: (-1,0),
    NE: (0,1),
    NW: (-1,1),
    SE: (1,-1),
    SW: (0,-1),
}

def xy_from_line(line):
    for old, new in zip(('ne','nw','se','sw'), (NE,NW,SE,SW)):
        line = line.replace(old, new)

    x,y = 0,0
    for ch in line:
        xoff, yoff = offsets[ch]
        x, y = x+xoff, y+yoff
    return x,y

lines = [line.strip() for line in sys.stdin]

tiles = defaultdict(lambda: 1)
for line in lines:
    x,y = xy_from_line(line)
    tiles[(x,y)] ^= 1

num_black = len([tile for tile in tiles.values() if not tile])
print('part1:', num_black)
assert num_black == 497

# part 2
def count_neighbors(tiles, x, y):
    '''Counts the number of white neighbors to a tile'''
    count = 0
    for cdir, (xoff, yoff) in offsets.items():
        if tiles.get((x+xoff, y+yoff), 1):
            count += 1
    return count

def gen_neigbors_xy(x, y):
    for cdir, (xoff, yoff) in offsets.items():
        yield x+xoff, y+yoff

def step_life(tiles):
    tocheck = set(tiles)
    for x,y in tiles:
        tocheck |= set(gen_neigbors_xy(x,y))

    oldtiles = tiles.copy()
    for pos in tocheck:
        color = oldtiles[pos]
        num_black = 6 - count_neighbors(oldtiles, *pos)
        if color == BLACK and (num_black == 0 or num_black > 2):
            tiles[pos] = WHITE
        elif color == WHITE and num_black == 2:
            tiles[pos] = BLACK

for i in range(100):
    step_life(tiles)

num_black = len([tile for tile in tiles.values() if not tile])
print('part2:', num_black)
assert num_black == 4156
