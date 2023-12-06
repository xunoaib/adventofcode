#!/usr/bin/env python3
import re
import sys
from z3 import Int, Optimize


def main():
    lines = sys.stdin.read().strip().split('\n')

    times, distances = [
        list(map(int, re.findall(r'\d+', line))) for line in lines
    ]

    ans1 = 1
    for time, dist in zip(times, distances):
        ways = 0
        for speed in range(1, time + 1):
            timeleft = time - speed
            if timeleft * speed > dist:
                ways += 1
        ans1 *= ways

    time = int(''.join(map(str, times)))
    dist = int(''.join(map(str, distances)))

    speed = Int('speed')
    s = Optimize()
    s.add(speed * (time - speed) > dist)
    s.push()
    s.minimize(speed)
    s.check()
    m = s.model()
    lowbound = m[speed].as_long()
    s.pop()

    # define upper bound for speed by adding a constraint that speed+1 is invalid.
    # otherwise, the optimizer will fail to return a true max
    s.add((speed + 1) * (time - (speed + 1)) <= dist)

    s.maximize(speed)
    s.check()
    m = s.model()
    highbound = m[speed].as_long()

    ans2 = highbound - lowbound + 1

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 2756160
    assert ans2 == 34788142


if __name__ == '__main__':
    main()
