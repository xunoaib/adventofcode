#!/usr/bin/env python3
import copy
import sys


def allcoords(brick):
    (x1, y1, z1), (x2, y2, z2) = brick
    ret = []
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                ret.append((x, y, z))
    return ret


def can_settle_brick(brick, world):
    coords = allcoords(brick)
    for x, y, z in coords:
        npos = (x, y, z - 1)
        if z <= 1 or (npos in world and npos not in coords):
            return False
    return True


def settle_step(bricks, world):
    changed = False
    for i, brick in enumerate(bricks):
        if can_settle_brick(brick, world):
            newspots = [(x, y, z - 1) for x, y, z in allcoords(brick)]
            for spot in allcoords(brick):
                del world[spot]
            world |= {spot: i for spot in newspots}
            bricks[i] = [newspots[0], newspots[-1]]
            changed = True
    return changed


def main():
    lines = sys.stdin.read().strip().split('\n')

    bricks = []
    world = {}
    for line in lines:
        brick = [list(map(int, g.split(','))) for g in line.split('~')]
        world |= {pos: len(bricks) for pos in allcoords(brick)}
        bricks.append(brick)

    while settle_step(bricks, world):
        pass

    a2 = 0
    canremove = set()
    for b, brick in enumerate(bricks):
        newgrid = {p: i for p, i in world.items() if i != b}
        rembricks = [br for br in bricks if br != brick]
        newbricks = copy.deepcopy(rembricks)
        if not settle_step(newbricks, newgrid):
            canremove.add(b)
        else:
            while settle_step(newbricks, newgrid):
                pass
            a2 += sum(1 for a, b in zip(rembricks, newbricks) if a != b)

    a1 = len(canremove)

    print('part1:', a1)
    print('part2:', a2)

    assert a1 == 468
    assert a2 == 75358


if __name__ == '__main__':
    main()
