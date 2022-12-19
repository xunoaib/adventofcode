#!/usr/bin/env python3
import sys

offsets = {(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, -1), (0, 0, 1)}

def add(p1, p2):
    return tuple(sum(x) for x in zip(p1, p2))

def main():
    lava = [tuple(map(int, line.split(','))) for line in sys.stdin]
    air = set()

    ans1 = 0
    for point in lava:
        for offset in offsets:
            newpt = add(point, offset)
            if newpt not in lava:
                ans1 += 1
                air.add(newpt)
    print('part1:', ans1)

    # connect all diagonally-adjacent air tiles by looking for adjacent air in each direction
    dilated = air.copy()
    for point in air:
        for offset in offsets:
            newpt = add(point, offset)
            if newpt not in lava:
                dilated.add(newpt)

    # discover and remove all external air tiles.
    # max(dilated) is guaranteed to be external
    q = [max(dilated)]
    while q:
        point = q.pop()
        for offset in offsets:
            newpt = add(point, offset)
            if newpt in dilated:
                dilated.remove(newpt)
                q.append(newpt)

    # count internal air/lava boundaries
    ans2 = ans1
    for point in dilated:
        for offset in offsets:
            newpt = add(point, offset)
            if newpt in lava:
                ans2 -= 1
    print('part2:', ans2)

    assert ans1 == 4314
    assert ans2 == 2444

if __name__ == '__main__':
    main()
