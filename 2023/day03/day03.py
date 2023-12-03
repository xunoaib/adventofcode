#!/usr/bin/env python3
import re
import string
import sys


def get_neighbors(r, c):
    for roff in [-1, 0, 1]:
        for coff in [-1, 0, 1]:
            if not (roff == coff == 0):
                yield r + roff, c + coff


def main():
    lines = sys.stdin.read().strip().split('\n')

    grid = {}
    syms = []  # symbol positions
    numid_vals = {}  # part number ids (unique) => actual part number
    pos_numid = {}  # (r,c) => part number id

    # convert input to dict and collect symbol positions
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            grid[r, c] = ch
            if ch in '!"#$%&\'()*+,-/:;<=>?@[\\]^_`{|}~':
                syms.append((r, c))

    # give each part number (having 1+ digits) a unique identifier, and create
    # a lookup table associating that id with each position the number occupies
    for r, line in enumerate(lines):
        for match in re.finditer(r'[0-9]+', line):
            num = int(match.group())
            num_id = len(numid_vals)
            numid_vals[num_id] = num
            for c in range(*match.span()):
                pos_numid[r, c] = num_id

    ans2 = ans1 = 0
    for pos in syms:
        numids = set()  # avoid counting the same number twice
        for npos in get_neighbors(*pos):
            if grid.get(npos, '.') in string.digits:
                numids.add(pos_numid[npos])

        nums = [numid_vals[n] for n in numids]
        ans1 += sum(nums)

        if grid[pos] == '*' and len(numids) == 2:
            ans2 += nums[0] * nums[1]

    print('part1:', ans1)
    print('part2:', ans2)

    assert ans1 == 536576
    assert ans2 == 75741499


if __name__ == '__main__':
    main()
