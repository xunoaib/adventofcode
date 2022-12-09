#!/usr/bin/env python3
import sys

dirs = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}


def step_knot(hr, hc, tr, tc):
    diffr = hr - tr
    diffc = hc - tc
    adr = abs(diffr)
    adc = abs(diffc)

    if {adr, adc} in [{1, 2}, {2}]:
        tr += diffr // adr
        tc += diffc // adc

    elif adr == 2:
        tr += diffr // adr

    elif adc == 2:
        tc += diffc // adc

    return tr, tc


def main():
    lines = sys.stdin.read().strip().split('\n')

    p1visited = set()
    p2visited = set()

    knots = [(0, 0)] * 10
    for line in lines:
        d, n = line.split(' ')
        dr, dc = dirs[d]
        for _ in range(int(n)):
            # update head knot
            hr, hc = knots[0]
            knots[0] = (hr + dr, hc + dc)

            # update subsequent knots
            for i, (r, c) in enumerate(knots[1:], start=1):
                knots[i] = step_knot(*knots[i - 1], r, c)

            p1visited.add(knots[1])
            p2visited.add(knots[-1])

    ans1 = len(p1visited)
    ans2 = len(p2visited)

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 5981
    assert ans2 == 2352


if __name__ == '__main__':
    main()
