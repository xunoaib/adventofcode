#!/usr/bin/env python
import sys

# row-col offsets for each direction (8 total)
DIRS = [(r,c) for r in (-1,0,1) for c in (-1,0,1) if (r,c) != (0,0)]

def count_neighbors1(grid, r, c):
    '''Count the number of occupied seats adjacent to a tile'''
    count = 0
    for roff, coff in DIRS:
        count += grid.get((r+roff, c+coff), 0)
        if count >= 4:
            break # exit early
    return count

def count_neighbors2(grid, r, c):
    '''Count the number of occupied seats in every extended direction'''
    count = 0
    for roff, coff in DIRS:
        count += find_first_neighbor(grid, r, c, roff, coff)
        if count >= 5:
            break # exit early
    return count

def find_first_neighbor(grid, row, col, roff, coff):
    '''Returns the first neighbor in the given extended direction:
        1 if occupied, 0 if empty or not found
    '''
    while 0 <= row < rows and 0 <= col < cols:
        row += roff
        col += coff
        val = grid.get((row,col))
        if val is not None:
            return val
    return 0

def step_life(grid, count_func, max_neighbors):
    '''Run a step of life with parameterized neighbor rules'''
    oldgrid = grid.copy()
    changed = False
    for (r,c), val in oldgrid.items():
        count = count_func(oldgrid, r, c)
        if val == 0 and count == 0:
            grid[(r,c)] = 1
            changed = True
        elif val and count >= max_neighbors:
            grid[(r,c)] = 0
            changed = True
    return changed

def print_grid(grid):
    for r in range(rows):
        for c in range(cols):
            print(grid.get((r,c), '.'), end='')
        print('')
    print('')

def run_simulation(count_func, max_neighbors, grid):
    i = 0
    while step_life(grid, count_func, max_neighbors):
        i += 1

    num_occupied = sum(grid.values())
    print('stable after turn', i)
    print('occupied seats:', num_occupied)

# create some nasty globals: row, col
grid = {}
for r, line in enumerate(sys.stdin):
    cols = len(line) - 1
    for c, char in enumerate(line.strip()):
        if char != '.':
            grid[(r,c)] = int(char == '#')
rows = r + 1

run_simulation(count_neighbors1, 4, grid.copy())
run_simulation(count_neighbors2, 5, grid.copy())
