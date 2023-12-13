#!/usr/bin/env python3
import sys


def vreflect(lines, r):
    upper, lower = lines[:r], lines[r:]
    upper = upper[::-1]
    return all(a == b for a, b in zip(upper, lower))


def vert_sym(lines):
    for r in range(1, len(lines)):
        if vreflect(lines, r):
            return r


def horiz_sym(lines):
    lines = [''.join(line[c] for line in lines) for c in range(len(lines[0]))]
    return vert_sym(lines)


def main():
    patterns = sys.stdin.read().strip().split('\n\n')
    a1 = 0

    for pat in patterns:
        lines = pat.split('\n')

        if v := vert_sym(lines):
            a1 += v * 100

        if h := horiz_sym(lines):
            a1 += h

    print('part1:', a1)


if __name__ == '__main__':
    main()
