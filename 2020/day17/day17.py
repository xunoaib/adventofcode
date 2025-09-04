#!/usr/bin/env python
import sys

X,Y,Z,W = 0,1,2,3

def count_neighbors(grid, x, y, z, w):
    '''Count the number of occupied seats adjacent to a tile'''
    count = 0
    for xoff, yoff, zoff, woff in DIRS:
        count += grid.get((x+xoff, y+yoff, z+zoff, w+woff), 0)
    return count

def step_life(grid):
    oldgrid = grid.copy()
    for pos in iter_grid_range(grid):
        val = oldgrid.get(pos, 0)
        count = count_neighbors(oldgrid, *pos)
        if val == 1 and count not in (2,3):
            del grid[(pos)]
        elif val == 0 and count == 3:
            grid[(pos)] = 1

def find_range(grid):
    '''Find the minimum and maximum used coordinates for each dimension'''
    maxs, mins = [], []
    for i in range(4):
        maxfound = max(key[i] for key in grid.keys())
        minfound = min(key[i] for key in grid.keys())
        maxs.append(maxfound)
        mins.append(minfound)
    return mins, maxs

def iter_grid_range(grid):
    '''Generate all points that need to be checked, including those 1 unit beyond the simulation area'''
    mins, maxs = find_range(grid)
    for x in range(mins[X]-1, maxs[X]+2):
        for y in range(mins[Y]-1, maxs[Y]+2):
            for z in range(mins[Z]-1, maxs[Z]+2):
                for w in range(mins[W]-1, maxs[W]+2):
                    yield x,y,z,w

def run_simulation(grid, num_steps=6):
    for i in range(num_steps):
        step_life(grid)
    return sum(grid.values())

grid = {}
for y, line in enumerate(sys.stdin):
    cols = len(line) - 1
    for x, char in enumerate(line.strip()):
        if char == '#':
            grid[(x,y,0,0)] = 1
rows = y + 1

DIRS = [(x,y,z,0) for x in (-1,0,1) for y in (-1,0,1) for z in (-1,0,1) if (x,y,z) != (0,0,0)]
num_occupied = run_simulation(grid.copy())
print('part1:', num_occupied)

DIRS = [(x,y,z,w) for x in (-1,0,1) for y in (-1,0,1) for z in (-1,0,1) for w in (-1,0,1) if (x,y,z,w) != (0,0,0,0)]
num_occupied = run_simulation(grid.copy())
print('part2:', num_occupied)
