#!/usr/bin/env python3
import sys
from itertools import combinations

def measure_paper(line):
    dims = list(map(int, line.split('x')))
    areas = list(a * b for a, b in combinations(dims, 2))
    return 2 * sum(areas) + min(areas)

def measure_ribbon(line):
    dims = list(map(int, line.split('x')))
    length = min(2 * (a + b) for a, b in combinations(dims, 2))
    return length + dims[0] * dims[1] * dims[2]

def main():
    lines = sys.stdin.read().strip().split()

    ans1 = sum(map(measure_paper, lines))
    print('part1:', ans1)

    ans2 = sum(map(measure_ribbon, lines))
    print('part2:', ans2)

    assert ans1 == 1588178
    assert ans2 == 3783758

if __name__ == '__main__':
    main()
