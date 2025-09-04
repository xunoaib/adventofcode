#!/usr/bin/env python
import sys
import math

grid = [line.strip() for line in sys.stdin]

def count_trees(roff, coff):
    r, c = (0, 0)
    trees = 0
    while r < len(grid):
        if grid[r][c % len(grid[0])] == '#':
            trees += 1
        r += roff
        c += coff
    return trees

print('part1:', count_trees(1,3))

slopes = [(1,1), (1,3), (1,5), (1,7), (2,1)]
product = math.prod(count_trees(*slope) for slope in slopes)

print('part2:', product)
