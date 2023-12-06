#!/usr/bin/env python3
import re
import sys


def translate_one(m, v):
    for d, s, r in m:
        if s <= v <= s + r:
            return v - s + d
    return v

def translate(maps, v):
    for m in maps:
        v = translate_one(m, v)
    return v

def inrange(v, startend):
    return startend[0] <= v <= startend[1]

def find_overlaps(segs1, segs2):
    segs1, segs = sorted(segs1), sorted(segs2)
    points = []

    for (p1x1, p1x2) in segs1:
        for (p2x1, p2x2) in segs2:
            if 

def main():
    lines = sys.stdin.read().strip().split('\n\n')
    # __import__('pprint').pprint(lines)

    seeds = list(map(int, lines[0].split(':')[1].strip().split(' ')))

    maps = []
    for group in lines[1:]:
        maps.append([])
        for line in group.split('\n')[1:]:
            maps[-1].append(tuple(map(int, line.split())))

    ans1 = min(translate(maps, s) for s in seeds)
    # print('part1:', ans1)

    ans2 = sys.maxsize

    ranges = []
    for m in maps:
        ranges.append([])
        for d,s,r in m:
            # ranges[-1].append((s, s+r, d, d+r))
            ranges[-1].append(((d, d+r), (s, s+r)))
        ranges[-1].sort()

    m1 = ranges[0]

    # __import__('pprint').pprint(m1)

    for m2 in ranges[1:]:
        # goal is to map src1 to dst2 by finding overlaps between dst1 and src2
        # (src_start1, src_end1), (dst_start1, dst_end1) = m1
        # (src_start2, src_end2), (dst_start2, dst_end2) = m2
        p1s = sorted(m1) # by dst
        p2s = sorted(m2, key=lambda kv: kv[-1])
        __import__('pprint').pprint(p1s)
        exit(0)

        # for seg1, seg2 in p1s[0]:

    # __import__('pprint').pprint(ranges[0])
    # __import__('pprint').pprint(ranges[1])

    # simp = list(maps[0])
    # newsimp = []
    # for d,s,r in maps[1]:

    # for i, m in enumerate(maps[1:]):
    #

    # __import__('pprint').pprint(maps[0])
    # print()
    # __import__('pprint').pprint(maps[-1])

    # ans2 = part2(lines)
    # print('part2:', ans2)

    # assert ans1 == 0
    # assert ans2 == 0


if __name__ == '__main__':
    main()
