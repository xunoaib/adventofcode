#!/usr/bin/env python3
import re
import sys
from collections import Counter


def genpoints(x1, x2, y1, y2, z1, z2):
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                yield x, y, z


def part1(cubes):
    """Naive solution for part 1"""
    on = set()
    for sign, cube in cubes:
        if any(abs(v) > 50 for v in cube):
            continue

        xr, yr, zr = [cube[i:i + 2] for i in range(0, 5, 2)]
        for x, y, z in genpoints(*xr, *yr, *zr):
            if sign == 1:
                on.add((x, y, z))
            else:
                on.discard((x, y, z))
    return len(on)


def intersects(c1, c2):
    xmin1, xmax1, ymin1, ymax1, zmin1, zmax1 = c1
    xmin2, xmax2, ymin2, ymax2, zmin2, zmax2 = c2
    return all([
        xmax1 > xmin2,
        xmin1 < xmax2,
        ymax1 > ymin2,
        ymin1 < ymax2,
        zmax1 > zmin2,
        zmin1 < zmax2,
    ])


def intersection(c1, c2):
    if intersects(c1, c2):
        xmin1, xmax1, ymin1, ymax1, zmin1, zmax1 = c1
        xmin2, xmax2, ymin2, ymax2, zmin2, zmax2 = c2
        return (max(xmin1, xmin2), min(xmax1, xmax2), max(ymin1, ymin2),
                min(ymax1, ymax2), max(zmin1, zmin2), min(zmax1, zmax2))


def volume(cube):
    pt1 = cube[::2]
    pt2 = cube[1::2]
    vals = [abs(d2 - d1) + 1 for d1, d2 in zip(pt1, pt2)]
    return vals[0] * vals[1] * vals[2]


def part2(cubes):
    regions = Counter()
    # for each new cube, look for existing intersections and cancel them out
    for sign1, c1 in cubes:
        for c2, sign2 in list(regions.items()):
            if cubeint := intersection(c1, c2):
                regions[cubeint] -= sign2  # cancel out this region's value

        if sign1 == 1:
            regions[c1] += sign1  # add region for "on" lights

    return sum(sign * volume(cube) for cube, sign in regions.items())


def main():
    cubes = []
    for line in sys.stdin:
        fields = re.match(r'(\S+) x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)', line).groups()
        cubes.append((1 if fields[0] == 'on' else -1, tuple(map(int, fields[1:]))))

    ans1 = part1(cubes)
    print('part1:', ans1)

    ans2 = part2(cubes)
    print('part2:', ans2)

    assert ans1 == 609563
    assert ans2 == 1234650223944734


if __name__ == '__main__':
    main()
