#!/usr/bin/env python3
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


def main():
    lines = sys.stdin.read().strip().split('\n\n')
    seeds = list(map(int, lines[0].split(':')[1].strip().split(' ')))
    maps = []

    for group in lines[1:]:
        maps.append([])
        for line in group.split('\n')[1:]:
            maps[-1].append(tuple(map(int, line.split())))

    ans1 = min(translate(maps, s) for s in seeds)
    print('part1:', ans1)

    ans2 = sys.maxsize
    for a, b in [seeds[i:i + 2] for i in range(0, len(seeds), 2)]:
        print('range:', a, b)
        for s in range(a, a + b):
            v = translate(maps, s)
            if v < ans2:
                print(f'{v=}')
                ans2 = v
        print('best:', ans2)
    print('part2:', ans2)


if __name__ == '__main__':
    main()
