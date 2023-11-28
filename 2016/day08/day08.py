#!/usr/bin/env python3
import re
import sys
import numpy as np

def main():
    lines = sys.stdin.readlines()
    screen = np.zeros((6,50), dtype=int)

    for line in lines:
        if m := re.match('rect (.*)x(.*)', line):
            a,b = map(int, m.groups())
            screen[:b,:a] = 1
        elif m := re.match('rotate row y=(.*) by (.*)', line):
            a,b = map(int, m.groups())
            # lazily perform 1-cell rotation B times
            for _ in range(b):
                screen[a] = np.append(screen[a,-1:], screen[a,:-1])
        elif m := re.match('rotate column x=(.*) by (.*)', line):
            a,b = map(int, m.groups())
            for _ in range(b):
                screen[:,a] = np.append(screen[-1:,a], screen[:-1,a])

    part1 = np.count_nonzero(screen == 1)
    print('part1:', part1)

    s = '\n'.join(
        ''.join('#' if ch else ' ' for ch in row)
        for row in screen
    )
    print(s)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
