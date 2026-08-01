#!/usr/bin/env python3
import sys

def print_grid(points):
    width, height = [max(vals) + 1 for vals in zip(*points)]
    grid = [['.']*width for i in range(height)]
    for x,y in points:
        grid[y][x] = '#'
    print('')
    print('\n'.join(''.join(row) for row in grid))
    print('')

def flipx(points, x_line):
    new_points = set()
    for x,y in points.copy():
        if x >= x_line:
            new_points.add((2 * x_line - x, y))
            points.remove((x,y))
    points.update(new_points)
    realign(points)

def flipy(points, y_line):
    new_points = set()
    for x,y in points.copy():
        if y >= y_line:
            new_points.add((x, 2 * y_line - y))
            points.remove((x,y))
    points.update(new_points)
    realign(points)

def realign(points):
    """Realign all coordinates relative to (0,0) to avoid negatives """
    minx, miny = map(min, zip(*points))
    new_points = set()
    for x,y in points:
        new_points.add((x-minx, y-miny))
    points.clear()
    points.update(new_points)

def run_command(points, axis, pos):
    if axis == 'x':
        flipx(points, int(pos))
    else:
        flipy(points, int(pos))

def part1(points, cmds):
    points = points.copy()
    run_command(points, *cmds[0])
    return len(points)

def part2(points, cmds):
    points = points.copy()
    for cmd in cmds:
        run_command(points, *cmd)
    print_grid(points)

def main():
    points, cmds = [group.split('\n') for group in sys.stdin.read().strip().split('\n\n')]
    points = set(tuple(map(int, line.split(','))) for line in points)
    cmds = [cmd.split(' ')[-1].split('=') for cmd in cmds]

    ans1 = part1(points, cmds)
    print('part1:', ans1)

    part2(points, cmds)

    assert ans1 == 770
    # assert ans2 == 'EPUELPBR'

if __name__ == '__main__':
    main()
