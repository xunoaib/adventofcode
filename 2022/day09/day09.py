#!/usr/bin/env python3
# import copy
# import re
# import numpy as np
# from collections import defaultdict
# from itertools import permutations
import sys

dirs = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

def main():
    lines = sys.stdin.read().strip().split('\n')

    visited = {(0,0)}

    hr = hc = tr = tc = 0
    for line in lines:
        d, n = line.split(' ')
        dr, dc = dirs[d]
        for _ in range(int(n)):
            hr += dr
            hc += dc

            diffr = hr - tr
            diffc = hc - tc

            adr = abs(diffr)
            adc = abs(diffc)

            if adr >= 2 and adc >= 2:
                print('b', end=' ')
                tr += diffr // adr
                tc += diffc // adc

            elif (adr, adc) == (1,2):
                tr += diffr // adr
                tc += diffc // adc

            elif (adr, adc) == (2,1):
                tc += diffc // adc
                tr += diffr // adr

            elif adr >= 2:
                print('r', end=' ')
                tr += diffr // adr

            elif adc >= 2:
                print('c', end=' ')
                tc += diffc // adc
            else:
                print(' ', end=' ')

            visited.add((tr, tc))
            print((diffr, diffc), (hr,hc), (tr,tc))
        print()

    # ans1 = part1(lines)
    print('part1:', len(visited))

    # ans2 = part2(lines)
    # print('part2:', ans2)

    # assert ans1 == 0
    # assert ans2 == 0

if __name__ == '__main__':
    main()
